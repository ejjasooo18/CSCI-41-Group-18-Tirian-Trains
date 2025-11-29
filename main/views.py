from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from .forms import SignUpForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Trip, Ticket, Customer

@login_required
def trip_list(request):
    # fetches all the trips ordered by trip date and departure time.
    trips = Trip.objects.all().order_by('trip_date', 'departure_time')
    return render(request, 'main/trip_list.html', {'trips': trips})

@login_required
def buy_ticket(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)

    if request.method == 'POST':
        # 1. Get the PASSENGER'S name from the form (curated by you)
        given_name = request.POST.get('given_name')
        surname = request.POST.get('surname')

        # 2. Create/Find the Customer (The person RIDING the train)
        passenger, created = Customer.objects.get_or_create(
            given_name=given_name,
            surname=surname,
            defaults={'middle_initial': 'X', 'gender': 'M', 'birth_date': '2000-01-01'}
        )

        # 3. Create the Ticket
        ticket_cost = trip.route.price if trip.route else 0
        
        ticket = Ticket.objects.create(
            owner=passenger,              # The name on the ticket (e.g., Mom)
            booked_by=request.user,       # YOUR account (The one paying)
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
    """
    The Dashboard.
    Displays: Hello {name}, Next Trip, and Action Buttons.
    """
    user = request.user
    
    # --- UPDATED LOGIC START ---
    # Instead of matching First/Last names (which can be empty or mismatched),
    # we simply find all tickets that are linked to your account via 'booked_by'.
    tickets = Ticket.objects.filter(booked_by=user)
    # --- UPDATED LOGIC END ---

    next_trip = None
    
    # --- YOUR ORIGINAL LOGIC BELOW (Preserved) ---
    # Look through all trips in those tickets, filter for future dates
    future_trips = []
    now = timezone.now().date()
    
    for ticket in tickets:
        for trip in ticket.trips.all():
            if trip.trip_date >= now:
                future_trips.append(trip)
    
    # Sort by date and pick the first one
    if future_trips:
        # (I added 'departure_time' to the sort so it's even more accurate, 
        # but the logic is the same as yours!)
        future_trips.sort(key=lambda x: (x.trip_date, x.departure_time))
        next_trip = future_trips[0]

    return render(request, 'main/home.html', {
        'user': user,
        'next_trip': next_trip
    })

@login_required
def my_trips(request):
    """
    Shows a list of all tickets bought by the currently logged-in user,
    regardless of whose name is on the ticket.
    """
    # Simple and Robust! 
    # Give me all tickets where 'booked_by' is ME.
    tickets = Ticket.objects.filter(booked_by=request.user).order_by('-date_booked')

    return render(request, 'main/my_trips.html', {'tickets': tickets})


def register(request):
    if request.method == 'POST':
        # Use your custom form here
        form = SignUpForm(request.POST) 
        if form.is_valid():
            form.save() # This saves the User AND their First/Last names
            return redirect('login')
    else:
        # Use your custom form here too
        form = SignUpForm()
    
    return render(request, 'registration/register.html', {'form': form})