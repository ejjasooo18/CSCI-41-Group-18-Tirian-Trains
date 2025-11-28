from django.shortcuts import render
from .models import Trip, Ticket, Customer

def trip_list(request):
    # fetches all the trips ordered by trip date and departure time.
    trips = Trip.objects.all().order_by('trip_date', 'departure_time')
    return render(request, 'main/trip_list.html', {'trips': trips})

