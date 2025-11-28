from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Trip, Ticket, Customer

def trip_list(request):
    # fetches all the trips ordered by trip date and departure time.
    trips = Trip.objects.all().order_by('trip_date', 'departure_time')
    return render(request, 'main/trip_list.html', {'trips': trips})

def buy_ticket(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)

    if request.method == 'POST':
        # get data from the HTML form
        given_name = request.POST.get('given_name')
        surname = request.POST.get('surname')

        # 1. find or create the Customer
        # we use get_or_create so we don't duplicate customers with the exact same name
        customer, created = Customer.objects.get_or_create(
            given_name=given_name,
            surname=surname,
            defaults={
                'middle_initial': 'X', # Placeholder
                'gender': 'M',         # Placeholder
                'birth_date': '2000-01-01' # Placeholder
            }
        )

        # 2. calculate Cost (price comes from the route)
        # note: our model has 'price' on Route, not trip.
        ticket_cost = trip.route.price if trip.route else 0

        # 3. create the Ticket
        ticket = Ticket.objects.create(
            owner=customer,
            total_cost=ticket_cost,
            date_booked=timezone.now().date(),
            date_expiration=timezone.now().date() # Placeholder expiration
        )

        # 4. link the Trip (many-to-many)
        ticket.trips.add(trip)

        return render(request, 'main/ticket_success.html', {'ticket': ticket})

    return render(request, 'main/buy_ticket_form.html', {'trip': trip})
