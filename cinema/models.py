from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import JSONField

class Movie(models.Model):
    title = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0,
                                 validators=[MinValueValidator(0), MaxValueValidator(10)])
    mrp = models.PositiveIntegerField(default=250)
    description = models.TextField(blank=True)
    featured = models.BooleanField(default=False)  # for carousel
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    date = models.DateField()
    time = models.TimeField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    gold_price = models.PositiveIntegerField(default=350)
    silver_price = models.PositiveIntegerField(default=250)
    # Track booked seats as list e.g. ["A1","A2"] stored in JSON
    booked_seats = JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date','time']

    def __str__(self):
        return f"{self.movie.title} — {self.date} {self.time}"

    def is_seat_booked(self, seat_label):
        return seat_label in (self.booked_seats or [])

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='bookings')
    seats = JSONField()   # ["G1", "S5"]
    total_cost = models.PositiveIntegerField()
    booked_at = models.DateTimeField(default=timezone.now)
    ticket_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Booking {self.ticket_id} by {self.user.username}"
