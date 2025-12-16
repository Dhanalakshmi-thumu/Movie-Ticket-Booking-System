from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Show, Booking
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
import uuid
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
from datetime import date
import pdfkit  # Make sure wkhtmltopdf is installed

# -------------------------
# HOME & SEARCH
# -------------------------
def home(request):
    featured = Movie.objects.filter(featured=True)[:4]
    movies = Movie.objects.all()
    return render(request, 'cinema/home.html', {'featured': featured, 'movies': movies})

def search(request):
    q = request.GET.get('q','').strip()
    movies = Movie.objects.filter(title__icontains=q) if q else Movie.objects.none()
    return render(request, 'cinema/search_results.html', {'query': q, 'movies': movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    shows = movie.shows.filter(date__gte=date.today()).order_by('date','time')
    return render(request, 'cinema/movie_detail.html', {'movie': movie, 'shows': shows})

# -------------------------
# SEAT SELECTION
# -------------------------
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Show


@login_required
def select_seats(request, show_id):
    show = get_object_or_404(Show, id=show_id)

    # -------------------------
    # Seat definitions
    # -------------------------
    GOLD_COUNT = 15
    SILVER_COUNT = 35

    gold_seats = [f"G{i}" for i in range(1, GOLD_COUNT + 1)]
    silver_seats = [f"S{i}" for i in range(1, SILVER_COUNT + 1)]
    all_seats = set(gold_seats + silver_seats)

    booked = set(show.booked_seats or [])

    # -------------------------
    # Helper: split into rows
    # -------------------------
    def chunk_list(lst, per_row):
        return [lst[i:i + per_row] for i in range(0, len(lst), per_row)]

    gold_rows = chunk_list(gold_seats, 5)     # 5 per row
    silver_rows = chunk_list(silver_seats, 7) # 7 per row

    # -------------------------
    # Handle POST (AJAX)
    # -------------------------
    if request.method == 'POST':
        selected = request.POST.getlist('seats[]')

        # ❗ Validate seat names
        if not selected or not all(s in all_seats for s in selected):
            return JsonResponse({
                'success': False,
                'message': 'Invalid seat selection'
            })

        with transaction.atomic():
            show = Show.objects.select_for_update().get(id=show_id)
            current_booked = set(show.booked_seats or [])

            # ❗ Prevent double booking
            if current_booked.intersection(selected):
                return JsonResponse({
                    'success': False,
                    'message': 'Some seats were already booked. Please refresh.'
                })

            # Calculate total
            total = sum(
                show.gold_price if s.startswith('G') else show.silver_price
                for s in selected
            )

            # Save pending booking in session
            request.session['pending_booking'] = {
                'show_id': show.id,
                'seats': selected,
                'total': total
            }

            return JsonResponse({
                'success': True,
                'redirect': f'/checkout/{show.id}/'
            })

    # -------------------------
    # GET request
    # -------------------------
    return render(request, 'cinema/select_seats.html', {
        'show': show,
        'gold_rows': gold_rows,
        'silver_rows': silver_rows,
        'booked': booked,
    })


# -------------------------
# CHECKOUT
# -------------------------
@login_required
def checkout(request, show_id):
    pending = request.session.get('pending_booking')
    if not pending or pending.get('show_id') != show_id:
        messages.error(request, "No pending booking. Please select seats first.")
        return redirect('movie_detail', movie_id=Show.objects.get(id=show_id).movie.id)

    show = get_object_or_404(Show, id=show_id)
    seats = pending['seats']
    total = pending['total']

    if request.method == 'POST':
        with transaction.atomic():
            show = Show.objects.select_for_update().get(id=show_id)
            if any(s in show.booked_seats for s in seats):
                messages.error(request, "Some seats were taken. Please reselect.")
                return redirect('select_seats', show_id=show_id)

            ticket_id = uuid.uuid4().hex[:12].upper()
            booking = Booking.objects.create(
                user=request.user,
                show=show,
                seats=seats,
                total_cost=total,
                ticket_id=ticket_id
            )
            show.booked_seats = (show.booked_seats or []) + seats
            show.save()

            del request.session['pending_booking']
            return redirect('success', ticket_id=ticket_id)

    return render(request, 'cinema/checkout.html', {'show': show, 'seats': seats, 'total': total})

# -------------------------
# BOOKING SUCCESS
# -------------------------
def success(request, ticket_id):
    booking = get_object_or_404(Booking, ticket_id=ticket_id)
    return render(request, 'cinema/success.html', {'booking': booking})

# -------------------------
# MY BOOKINGS
# -------------------------
@login_required
def my_bookings(request):
    bookings = request.user.bookings.order_by('-booked_at')
    return render(request, 'cinema/my_bookings.html', {'bookings': bookings})

# -------------------------
# SIGNUP
# -------------------------
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'cinema/signup.html', {'form': form})

# -------------------------
# DOWNLOAD TICKET PDF
# -------------------------
@login_required
def download_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    html = render_to_string('cinema/ticket_pdf.html', {'booking': booking})
    pdf = pdfkit.from_string(html, False)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Ticket_{booking.ticket_id}.pdf"'
    return response

# -------------------------
# CANCEL BOOKING
# -------------------------
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        with transaction.atomic():
            show = booking.show
            booked_seats = set(show.booked_seats or [])
            booked_seats.difference_update(booking.seats)
            show.booked_seats = list(booked_seats)
            show.save()
            booking.delete()

        messages.success(request, "Booking cancelled successfully!")
        return redirect('my_bookings')

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import A6
from reportlab.pdfgen import canvas
from .models import Booking

@login_required
def download_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Ticket_{booking.ticket_id}.pdf"'

    c = canvas.Canvas(response, pagesize=A6)
    width, height = A6

    # Simple ticket layout
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, height-40, booking.show.movie.title)

    c.setFont("Helvetica", 12)
    c.drawString(20, height-70, f"Date: {booking.show.date}")
    c.drawString(20, height-90, f"Time: {booking.show.time}")
    c.drawString(20, height-110, f"Seats: {', '.join(booking.seats)}")
    c.drawString(20, height-130, f"Ticket ID: {booking.ticket_id}")
    c.drawString(20, height-150, f"Price: ₹ {booking.total_cost}")

    c.showPage()
    c.save()

    return response

