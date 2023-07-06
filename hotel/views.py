from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Hotel, Invoice, Passenger, Image
from .serializers import HotelSerializer, InvoiceSerializer, PassengerSerializer, ImageCreateSerializer
from django.contrib.auth.models import User


class ImageCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        data = request.data
        hotel_name = data.pop('hotel', None)
        if hotel_name is not None:
            hotel_name = hotel_name[0]
        hotel = Hotel.objects.filter(name=hotel_name).first()
        if not hotel:
            return Response({'error': 'Hotel not found'}, status=status.HTTP_404_NOT_FOUND)
        data['hotel'] = hotel.id
        ser_data = ImageCreateSerializer(data=data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class HotelCreateRetrieveView(APIView):
    def get(self, request):
        hotels = Hotel.objects.all()
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)

    def post(self, request: Request):
        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceCreateView(APIView):
    def post(self, request):
        data = request.data
        hotel_name = data.pop('hotel', None)
        hotel = Hotel.objects.filter(name=hotel_name).first()
        if not hotel:
            return Response({'error': 'Hotel not found'}, status=status.HTTP_404_NOT_FOUND)
        user_name = data.pop('user', None)
        user = User.objects.filter(username=user_name).first()
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        data['hotel'] = hotel.id
        data['user'] = user.id
        serializer = InvoiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceRetrieveView(APIView):
    def get(self, request, invoice_id):
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return Response({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)
