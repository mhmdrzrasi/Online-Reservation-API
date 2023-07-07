from django.contrib import admin
from .models import Plane, Invoice, Passenger


class PassengerInline(admin.TabularInline):
    model = Passenger
    extra = 1


@admin.register(Plane)
class PlaneAdmin(admin.ModelAdmin):
    list_display = ('id', 'capacity', 'departure_date', 'return_date')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'plane')
    inlines = [PassengerInline]
