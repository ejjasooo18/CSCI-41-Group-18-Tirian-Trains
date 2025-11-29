from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Trip, Ticket, Customer

def trip_list(request):
    # fetches all the trips ordered by trip date and departure time.
    trips = Trip.objects.all().order_by('trip_date', 'departure_time')
    return render(request, 'main/trip_list.html', {'trips': trips})

def buy_ticket(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)

    if request.method == 'POST':
        given_name = request.POST.get('given_name')
        surname = request.POST.get('surname')

  
        if request.user.is_authenticated:
            request.user.first_name = given_name
            request.user.last_name = surname
            request.user.save() 

        customer, created = Customer.objects.get_or_create(
            given_name=given_name,
            surname=surname,
            defaults={
                'middle_initial': 'X', 
                'gender': 'M',        
                'birth_date': '2000-01-01'
            }
        )

        ticket_cost = trip.route.price if trip.route else 0

        ticket = Ticket.objects.create(
            owner=customer,
            total_cost=ticket_cost,
            date_booked=timezone.now().date(),
            date_expiration=timezone.now().date()
        )

        ticket.trips.add(trip)

        return render(request, 'main/ticket_confirmation.html', {'ticket': ticket})

    context = {
        'trip': trip,
        'user_given_name': request.user.first_name,
        'user_surname': request.user.last_name
    }
    return render(request, 'main/buy_ticket.html', context)

@login_required
def home(request):
    """
    The Dashboard.
    Displays: Hello {name}, Next Trip, and Action Buttons.
    """
    user = request.user
    
    # PROTOTYPE LOGIC: 
    # We find the Customer that matches the logged-in User's name.
    # In a real app, we'd have a OneToOne link, but this works for now!
    customer = Customer.objects.filter(
        given_name=user.first_name, 
        surname=user.last_name
    ).first()

    next_trip = None
    if customer:
        # Find all tickets for this customer
        tickets = Ticket.objects.filter(owner=customer)
        
        # Look through all trips in those tickets, filter for future dates
        # Note: This is Python-side filtering because of the M:N relationship complexity
        future_trips = []
        now = timezone.now().date()
        
        for ticket in tickets:
            for trip in ticket.trips.all():
                if trip.trip_date >= now:
                    future_trips.append(trip)
        
        # Sort by date and pick the first one
        future_trips.sort(key=lambda x: x.trip_date)
        if future_trips:
            next_trip = future_trips[0]

    return render(request, 'main/home.html', {
        'user': user,
        'next_trip': next_trip
    })

@login_required
def my_trips(request):
    """
    Shows a list of all tickets bought by the user.
    """
    user = request.user
    # Match User -> Customer
    customer = Customer.objects.filter(
        given_name=user.first_name, 
        surname=user.last_name
    ).first()

    tickets = []
    if customer:
        tickets = Ticket.objects.filter(owner=customer).order_by('-date_booked')

    return render(request, 'main/my_trips.html', {'tickets': tickets})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})