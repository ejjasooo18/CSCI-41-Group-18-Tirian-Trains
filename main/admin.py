from django.contrib import admin

from .models import (Station,
                     Route,
                     Trip,
                     Customer,
                     Ticket,
                     Train,
                     CrewMember,
                     MaintenanceEvent)


class TicketInline(admin.TabularInline):
    model = Ticket
    filter_horizontal = ['trips']


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    inlines = [TicketInline,]


class TicketAdmin(admin.ModelAdmin):
    list_filter = ['owner', 'booked_by']
    filter_horizontal = ['trips']


class MaintenanceEventAdmin(admin.ModelAdmin):
    list_filter = ['train']


admin.site.register(Station)
admin.site.register(Trip)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Train)
admin.site.register(CrewMember)
admin.site.register(MaintenanceEvent, MaintenanceEventAdmin)
