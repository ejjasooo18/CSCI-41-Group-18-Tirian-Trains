from django.contrib import admin

from .models import (Station,
                     Route,
                     Trip,
                     Customer,
                     Ticket,
                     Train,
                     CrewMember,
                     MaintenanceEvent)


admin.site.register(Station)
admin.site.register(Route)
admin.site.register(Trip)
admin.site.register(Customer)
admin.site.register(Ticket)
admin.site.register(Train)
admin.site.register(CrewMember)
admin.site.register(MaintenanceEvent)
