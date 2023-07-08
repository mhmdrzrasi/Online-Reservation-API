from django.contrib import admin
from .models import Train, Invoice, Passenger


class PassengerInline(admin.TabularInline):
    model = Passenger
    extra = 1


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('id', 'capacity', 'departure_date', 'return_date')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'train')
    inlines = [PassengerInline]
