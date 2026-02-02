from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from .forms import SignUpForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Trip, Ticket, Customer

@login_required
def trip_list(request):
    # Fetches all the trips ordered by trip date and departure time.
    trips = Trip.objects.all().order_by('trip_date', 'departure_time')
    return render(request, 'main/trip_list.html', {'trips': trips})

@login_required
def buy_ticket(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)

    if request.method == 'POST':
        # 1. Get the PASSENGER'S name from the form curated by the logged-in user
        given_name = request.POST.get('given_name')
        surname = request.POST.get('surname')

        # 2. Create/Find the Customer which is the person that will ride the train 
        passenger, created = Customer.objects.get_or_create(
            given_name=given_name,
            surname=surname,
            defaults={'middle_initial': 'X', 'gender': 'M', 'birth_date': '2000-01-01'}
        )

        # 3. Create the Ticket
        ticket_cost = trip.route.price if trip.route else 0
        
        ticket = Ticket.objects.create(
            owner=passenger,              # The name on the ticket (e.g., Your boyfriend :>)
            booked_by=request.user,       # Your account (The one paying or the logged-in)
            total_cost=ticket_cost,
            date_booked=timezone.now().date(),
            date_expiration=timezone.now().date()
        )

        ticket.trips.add(trip)
        return render(request, 'main/ticket_confirmation.html', {'ticket': ticket})

    context = {
        'trip': trip,
        'default_given': request.user.first_name, 
        'default_surname': request.user.last_name
    }
    return render(request, 'main/buy_ticket.html', context)

@login_required
def home(request):
    user = request.user
    
    # 1. Find tickets booked by user
    tickets = Ticket.objects.filter(booked_by=user)
    
    future_trips = []
    now = timezone.now().date()
    
    # 2. Filter for future dates
    for ticket in tickets:
        for trip in ticket.trips.all():
            if trip.trip_date >= now:
                future_trips.append(trip)
    
    # 3. Sort by date/time
    if future_trips:
        future_trips.sort(key=lambda x: (x.trip_date, x.departure_time))
        
    upcoming_trips = future_trips[:3] 

    return render(request, 'main/home.html', {
        'user': user,
        'upcoming_trips': upcoming_trips 
    })

@login_required
def my_trips(request):
    """
    Shows a list of all tickets bought by the currently logged-in user,
    regardless of whose name is on the ticket.
    """
    tickets = Ticket.objects.filter(booked_by=request.user).order_by('-date_booked')

    return render(request, 'main/my_trips.html', {'tickets': tickets})


def register(request):
    if request.method == 'POST':

        form = SignUpForm(request.POST) 
        if form.is_valid():
            form.save() # This saves the User and their First/Last names
            return redirect('login')
    else:

        form = SignUpForm()
    
    return render(request, 'registration/register.html', {'form': form})