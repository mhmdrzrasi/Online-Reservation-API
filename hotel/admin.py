from django.contrib import admin
from .models import Hotel, Invoice, Passenger, Room, Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class RoomInline(admin.TabularInline):
    model = Room
    extra = 1


class PassengerInline(admin.TabularInline):
    model = Passenger
    extra = 1


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'stars', 'capacity')
    inlines = [RoomInline, ImageInline]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'hotel', 'beds', 'entry_date', 'leave_date')
    inlines = [PassengerInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'hotel')
