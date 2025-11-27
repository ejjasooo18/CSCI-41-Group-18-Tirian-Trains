from datetime import timedelta, date

from django.db import models
from django.core.validators import RegexValidator

ROUTE_TYPE = {
    'INT': 'Inter-town',
    'LOC': 'Local'
}

GENDER = {
    'F': 'Female',
    'M': 'Male'
}

CONDITION = {
    'worse': 'Worse',
    'bad': 'Bad',
    'good': 'Good',
    'vgood': 'Very Good',
    'excellent': 'Excellent'
}

no_symbols_except_dot = RegexValidator(r'^[0-9a-zA-Z. ]*$',
                                       'No symbols are allowed except \".\".')
model_format = RegexValidator(r'^[AS]-[0-9][0-9][0-9]$',
                              'Must follow the format \"A-###\" or \"S-###\".')


class Station(models.Model):
    station_name = models.CharField(max_length=255,
                                    default='Unnamed Station')

    def __str__(self):
        return f'S-{self.pk}: {self.station_name}'


class Route(models.Model):
    price = models.PositiveIntegerField(default=0)
    travel_time = models.DurationField(default=timedelta(minutes=5))
    route_type = models.CharField(default='LOC', choices=ROUTE_TYPE)
    destination = models.ForeignKey(
        Station,
        on_delete=models.SET_NULL,
        null=True,
        related_name='as_route_destinations'
    )
    origin = models.ForeignKey(
        Station,
        on_delete=models.SET_NULL,
        null=True,
        related_name='as_route_origins'
    )

    def __str__(self):
        return (f'R-{self.pk}: {self.origin.station_name} '
                f'-> {self.destination.station_name}')


class Trip(models.Model):
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.GeneratedField(
        expression=models.F('departure_time')-models.F('arrival_time'),
        output_field=models.DurationField(),
        db_persist=True
    )
    destination = models.ForeignKey(
        Station,
        on_delete=models.SET_NULL,
        null=True,
        related_name='as_trip_destinations'
    )
    origin = models.ForeignKey(
        Station,
        on_delete=models.SET_NULL,
        null=True,
        related_name='as_trip_origins'
    )
    trip_date = models.DateField(default=date.min)

    def __str__(self):
        return 'T-' + str(self.pk)


class Customer(models.Model):
    surname = models.CharField(max_length=255,
                               default='Rizal',
                               validators=[no_symbols_except_dot])
    given_name = models.CharField(max_length=255,
                                  default='Jose',
                                  validators=[no_symbols_except_dot])
    middle_initial = models.CharField(max_length=10,
                                      default='P.',
                                      validators=[no_symbols_except_dot])
    birth_date = models.DateField(default=date.min,
                                  null=True,
                                  blank=True)
    gender = models.CharField(max_length=1,
                              default='M',
                              choices=GENDER)

    def __str__(self):
        return f'{self.surname}, {self.given_name} {self.middle_initial}'

    class Meta:
        ordering = ['surname']


class Ticket(models.Model):
    total_cost = models.PositiveIntegerField(default=0)
    date_booked = models.DateField(default=date.min)
    date_expiration = models.DateField(default=date.min)
    owner = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    trips = models.ManyToManyField(Trip)

    def __str__(self):
        return f'Ticket No. {self.pk} {self.date_booked}'


class Train(models.Model):
    model = models.CharField(max_length=5,
                             default='S-000',
                             validators=[model_format])
    max_speed = models.PositiveIntegerField(default=0)
    no_of_seats = models.PositiveIntegerField(default=0)
    no_of_toilets = models.PositiveIntegerField(default=0)
    has_recling_seats = models.BooleanField(default=False)
    has_folding_tables = models.BooleanField(default=False)
    has_disability_access = models.BooleanField(default=False)
    has_luggage_storage = models.BooleanField(default=False)
    has_vending_machines = models.BooleanField(default=False)
    has_food_service = models.BooleanField(default=False)

    def __str__(self):
        return f'Train {self.pk}'


class CrewMember(models.Model):
    surname = models.CharField(max_length=255,
                               default='Rizal',
                               validators=[no_symbols_except_dot])
    given_name = models.CharField(max_length=255,
                                  default='Jose',
                                  validators=[no_symbols_except_dot])
    middle_initial = models.CharField(max_length=10,
                                      default='P.',
                                      validators=[no_symbols_except_dot])

    def __str__(self):
        return f'{self.surname}, {self.given_name} {self.middle_initial}'


class MaintenanceEvent(models.Model):
    event_date = models.DateField(default=date.min)
    task = models.CharField(max_length=255,
                            default='General Maintenance')
    condition = models.CharField(max_length=50,
                                 default='good',
                                 choices=CONDITION)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    crew_member = models.ForeignKey(CrewMember, on_delete=models.CASCADE)

    def __str__(self):
        return (f'{self.event_date}: {self.task} '
                f'on {self.train} by {self.crew_member}')

    class Meta:
        ordering = ['-event_date']
