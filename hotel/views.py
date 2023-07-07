from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from django.db.models import F, Sum, Q, Count

from .models import Hotel, Invoice, Passenger, Image, Room
from .serializers import HotelSerializer, InvoiceSerializer, PassengerSerializer, ImageCreateSerializer
from accounts.models import User


# Hotel

class HotelCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request: Request):
        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HotelUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request: Request, pk):
        hotel = get_object_or_404(Hotel, pk=pk)
        ser_data = HotelSerializer(instance=hotel, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class HotelDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request: Request, pk):
        hotel = get_object_or_404(Hotel, pk=pk)
        hotel.delete()
        return Response({'message': 'hotel deleted successfully'}, status=status.HTTP_200_OK)


class HotelGetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, pk):
        hotel = get_object_or_404(Hotel, pk=pk)
        ser_data = HotelSerializer(instance=hotel)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class HotelListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hotels = Hotel.objects.all()
        ser_data = HotelSerializer(hotels, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


# Invoice

class InvoiceCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        data = request.data

        hotel_name = data.pop('hotel', None)
        if hotel_name is not None:
            hotel = Hotel.objects.filter(name=hotel_name).first()
            if not hotel:
                return Response({'error': 'hotel not found'}, status=status.HTTP_404_NOT_FOUND)
            data['hotel'] = hotel.id

        ser_data = InvoiceSerializer(data=data, context={'user_id': request.user.id})
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request: Request, pk):
        data = request.data

        hotel_name = data.pop('hotel', None)
        if hotel_name is not None:
            hotel = Hotel.objects.filter(name=hotel_name).first()
            if not hotel:
                return Response({'error': 'hotel not found'}, status=status.HTTP_404_NOT_FOUND)
            data['hotel'] = hotel.id

        invoice = get_object_or_404(Invoice, pk=pk)
        ser_data = InvoiceSerializer(instance=invoice, data=data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)
        invoice.delete()
        return Response({'message': 'invoice deleted successfully'}, status=status.HTTP_200_OK)


class InvoiceGetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)
        ser_data = InvoiceSerializer(instance=invoice)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class InvoiceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        invoices = Invoice.objects.all()
        ser_data = InvoiceSerializer(instance=invoices, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


# Image

class ImageCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
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


class ImageDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request: Request, pk):
        image = get_object_or_404(Image, pk=pk)
        image.delete()
        return Response({'message': 'image deleted successfully'}, status=status.HTTP_200_OK)


# Filter

class FilterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        data = request.data
        new_data = None

        city = data.pop('city', None)
        entry_date = data.pop('entry_date', None)
        leave_date = data.pop('leave_date', None)
        passengers = data.pop('passengers', None)

        if city is not None and type(city) == str: new_data = Hotel.objects.filter(city=city)

        if entry_date is not None and leave_date is not None:

            capacity_query = Room.objects.values('hotel').annotate(capacity=Sum(F('number_of_rooms') * F('beds')))
            in_use_query = Invoice.objects.values('hotel').annotate(
                in_use=Count('passengers', filter=Q(entry_date__lte=leave_date, leave_date__gte=entry_date)))

            if new_data is not None:
                new_data = new_data.filter(
                    pk__in=[h['hotel'] for h in capacity_query if
                            h['capacity'] > (in_use_query.get(hotel=h['hotel'])['in_use'])])
            else:
                new_data = Hotel.objects.filter(
                    pk__in=[h['hotel'] for h in capacity_query if
                            h['capacity'] > (in_use_query.get(hotel=h['hotel'])['in_use'])]
                )

        if passengers is not None and (type(passengers) == str or type(passengers) == int):

            capacity_query = Room.objects.values('hotel').annotate(capacity=Sum(F('number_of_rooms') * F('beds')))
            in_use_query = Invoice.objects.values('hotel').annotate(in_use=Count('passengers'))

            if new_data is not None:
                new_data = new_data.filter(
                    pk__in=[h['hotel'] for h in capacity_query if
                            h['capacity'] >= (in_use_query.get(hotel=h['hotel'])['in_use'] + int(passengers))])
            else:
                new_data = Hotel.objects.filter(
                    pk__in=[h['hotel'] for h in capacity_query if
                            h['capacity'] >= (in_use_query.get(hotel=h['hotel'])['in_use'] + int(passengers))])

        if new_data is None:
            return Response({'message': 'filter is empty',
                             'hint': 'you can send : city - entry_date - leave_date - passengers'})
        elif not len(new_data):  # لیست خالی عه یعنی فیلتر هارو وارد کردند ولی هتلی پیدا نشده
            return Response({'message': 'Information matching the entries was not found'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            ser_data = HotelSerializer(instance=new_data, many=True)
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
