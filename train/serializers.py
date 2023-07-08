import re

from rest_framework import serializers
from .models import Train, Invoice, Passenger
from accounts.models import User


def check_national_id(value):
    if not re.match(r'^\d{10}$', value):
        raise serializers.ValidationError('national id should only be 10 digits')


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ['id', 'firstname', 'lastname', 'national_id', 'birthday', 'gender']
        extra_kwargs = {
            'national_id': {'validators': (check_national_id,)},
        }


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ['id', 'train_number', 'coupe_number', 'features',
                  'capacity', 'starting_city', 'destination_city', 'departure_date', 'return_date']


class InvoiceSerializer(serializers.ModelSerializer):
    passengers = PassengerSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['id', 'train', 'user', 'passengers']
        read_only_fields = ['user']

    def create(self, validated_data):
        passengers_data = validated_data.pop('passengers')
        invoice = Invoice.objects.create(user_id=self.context['user_id'], **validated_data)
        for passenger_data in passengers_data:
            Passenger.objects.create(invoice=invoice, **passenger_data)
        return invoice

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['train'] = instance.train.train_number
        data['user'] = instance.user.phone_number
        return data
