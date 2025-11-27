from datetime import timedelta

from django.db import models

ROUTE_TYPE = {
    'INT': 'Inter-town',
    'LOC': 'Local'
}


class Route(models.Model):
    price = models.PositiveIntegerField(default=0)
    travel_time = models.DurationField(default=timedelta(minutes=5))
    route_type = models.CharField(default='INT', choices=ROUTE_TYPE)


class Station(models.Model):
    pass


class Trip(models.Model):
    pass


class Customer(models.Model):
    pass


class Ticket(models.Model):
    pass


class Train(models.Model):
    pass


class MaintenanceEvent(models.Model):
    pass


class CrewMember(models.Model):
    pass

