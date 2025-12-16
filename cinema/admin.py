from django.contrib import admin
from .models import Movie, Show, Booking

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title','duration','rating','mrp','featured')
    list_filter = ('featured',)

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('movie','date','time','duration','gold_price','silver_price')
    list_filter = ('date','movie')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('ticket_id','user','show','total_cost','booked_at')
    readonly_fields = ('ticket_id','booked_at')
