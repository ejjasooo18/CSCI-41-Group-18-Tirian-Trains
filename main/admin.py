from django.contrib import admin

from .models import (Station,
                     Route,
                     Trip,
                     Customer,
                     Ticket,
                     Train,
                     CrewMember,
                     MaintenanceEvent)


class TicketAdmin(admin.ModelAdmin):
    filter_horizontal = ['trips']


admin.site.register(Station)
admin.site.register(Route)
admin.site.register(Trip)
admin.site.register(Customer)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Train)
admin.site.register(CrewMember)
admin.site.register(MaintenanceEvent)
