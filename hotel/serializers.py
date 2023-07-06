from rest_framework import serializers
from .models import Hotel, Invoice, Passenger, Room, Image
from accounts.models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ['id', 'firstname', 'lastname', 'national_id', 'phone_number', 'gender']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['number_of_rooms', 'beds']


class ImageCreateSerializer(serializers.ModelSerializer):
    hotel = serializers.CharField(max_length=128)

    class Meta:
        model = Image
        fields = ('id', 'image', 'hotel')

    def create(self, validated_data):
        hotel = validated_data.pop('hotel')
        image = Image.objects.create(hotel_id=hotel, **validated_data)
        return image


class HotelSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True)

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'city', 'stars', 'features', 'capacity', 'rooms']

    def create(self, validated_data):
        rooms_data = validated_data.pop('rooms')
        hotel = Hotel.objects.create(**validated_data)
        for room_data in rooms_data:
            Room.objects.create(hotel=hotel, **room_data)
        return hotel


class InvoiceSerializer(serializers.ModelSerializer):
    passengers = PassengerSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['id', 'entry_date', 'leave_date', 'hotel', 'user', 'beds', 'passengers']

    def create(self, validated_data):
        passengers_data = validated_data.pop('passengers')
        invoice = Invoice.objects.create(**validated_data)
        for passenger_data in passengers_data:
            Passenger.objects.create(invoice=invoice, **passenger_data)
        return invoice
