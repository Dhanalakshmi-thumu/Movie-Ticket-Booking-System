from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Home & Movies
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),

    # Seat selection & booking
    path('show/<int:show_id>/select-seats/', views.select_seats, name='select_seats'),
    path('checkout/<int:show_id>/', views.checkout, name='checkout'),
    path('success/<str:ticket_id>/', views.success, name='success'),

    # My Bookings
    path('mybookings/', views.my_bookings, name='my_bookings'),
    
    # Ticket actions
    path('download-ticket/<int:booking_id>/', views.download_ticket, name='download_ticket'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='cinema/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup, name='signup'),
]
