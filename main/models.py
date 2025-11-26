from django.db import models

class Station(models.Model):
    station_id = models.AutoField(primary_key=True)
    station_name = models.CharField(max_length=100)

    def __str__(self):
        return self.station_name

class Route(models.Model):
    route_id = models.CharField(max_length=10, primary_key=True) # e.g., "R-01"
    route_type = models.CharField(max_length=50) # Local/Inter-town
    travel_time = models.IntegerField(help_text="Time in minutes")
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    
    # relationships
    origin_station = models.ForeignKey(Station, related_name='routes_from', on_delete=models.CASCADE)
    destination_station = models.ForeignKey(Station, related_name='routes_to', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.route_id}: {self.origin_station} to {self.destination_station}"

class Train(models.Model):
    train_id = models.AutoField(primary_key=True)
    model = models.CharField(max_length=50)
    max_speed = models.IntegerField()
    no_of_seats = models.IntegerField()
    no_of_toilets = models.IntegerField()
    
    # booleans for features
    has_reclining_seats = models.BooleanField(default=False)
    has_folding_tables = models.BooleanField(default=False)
    has_disability_access = models.BooleanField(default=False)
    has_luggage_storage = models.BooleanField(default=False)
    has_vending_machines = models.BooleanField(default=False)
    has_food_service = models.BooleanField(default=False)

    def __str__(self):
        return f"Train {self.train_id} ({self.model})"

class Trip(models.Model):
    trip_id = models.AutoField(primary_key=True)
    trip_date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    cost = models.DecimalField(max_digits=6, decimal_places=2) # Specific trip cost
    
    # relationships
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)

    def __str__(self):
        return f"Trip {self.trip_id} on {self.trip_date}"

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=50)
    given_name = models.CharField(max_length=50)
    middle_initial = models.CharField(max_length=2, blank=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.given_name} {self.surname}"

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    date_booked = models.DateField(auto_now_add=True)
    date_expiration = models.DateField()
    ticket_year = models.IntegerField()
    
    # relationships
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    # many-to-many Relationship
    # this automatically creates the "TICKET_TRIP" bridge table in the background
    trips = models.ManyToManyField(Trip) 

    def __str__(self):
        return f"Ticket {self.ticket_id} for {self.customer}"

class CrewMember(models.Model):
    member_id = models.AutoField(primary_key=True)
    surname = models.CharField(max_length=50)
    given_name = models.CharField(max_length=50)
    initial = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return f"{self.given_name} {self.surname}"

class MaintenanceEvent(models.Model):
    maintenance_id = models.AutoField(primary_key=True)
    maintenance_date = models.DateField()
    task = models.CharField(max_length=100)
    condition = models.CharField(max_length=50)
    
    # relationships
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(CrewMember, on_delete=models.CASCADE)

    def __str__(self):
        return f"Maintenance {self.maintenance_id} on {self.train}"