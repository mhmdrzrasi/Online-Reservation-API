from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from django.db.models import F, Q, Sum, Count

from .models import Train, Invoice, Passenger
from .serializers import TrainSerializer, InvoiceSerializer, PassengerSerializer


# Train

class TrainCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request: Request):
        serializer = TrainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrainUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request: Request, pk):
        train = get_object_or_404(Train, pk=pk)
        ser_data = TrainSerializer(instance=train, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class TrainDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request: Request, pk):
        train = get_object_or_404(Train, pk=pk)
        train.delete()
        return Response({'message': 'Train deleted successfully'}, status=status.HTTP_200_OK)


class TrainGetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, pk):
        train = get_object_or_404(Train, pk=pk)
        ser_data = TrainSerializer(instance=train)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class TrainListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trains = Train.objects.all()
        ser_data = TrainSerializer(trains, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


# Invoice

class InvoiceCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        data = request.data

        train_number = data.pop('train', None)
        if train_number is not None:
            train = Train.objects.filter(train_number=train_number).first()
            if not train:
                return Response({'error': 'train not found'}, status=status.HTTP_404_NOT_FOUND)
            data['train'] = train.id

        ser_data = InvoiceSerializer(data=data, context={'user_id': request.user.id})
        if ser_data.is_valid():
            ser_data.save()
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request: Request, pk):
        data = request.data

        train_number = data.pop('train', None)
        if train_number is not None:
            train = Train.objects.filter(train_number=train_number).first()
            if not train:
                return Response({'error': 'train not found'}, status=status.HTTP_404_NOT_FOUND)
            data['train'] = train.id

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


class FilterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        new_data = None

        starting_city = data.pop('starting_city', None)
        destination_city = data.pop('destination_city', None)
        passengers = data.pop('passengers', None)
        departure_date = data.pop('departure_date', None)
        return_date = data.pop('return_date', None)

        if starting_city is not None and type(starting_city) == str:
            new_data = Train.objects.filter(starting_city=starting_city)

        if destination_city is not None and type(destination_city) == str:
            if new_data is not None:
                new_data = new_data.filter(destination_city=destination_city)
            else:
                new_data = Train.objects.filter(destination_city=destination_city)

        if departure_date is not None and type(departure_date) == str:
            if new_data is not None:
                new_data = new_data.filter(departure_date=departure_date)
            else:
                new_data = Train.objects.filter(departure_date=departure_date)

        if return_date is not None:
            if new_data is not None:
                new_data = new_data.filter(return_date=return_date)
            else:
                new_data = Train.objects.filter(return_date=return_date)

        if passengers is not None and (type(passengers) == str or type(passengers) == int):

            if new_data is not None:
                new_data = new_data.annotate(
                    num_passengers=Count('invoices_train__passengers')
                ).filter(capacity__gte=F('num_passengers') + str(passengers))
            else:
                new_data = Train.objects.annotate(
                    num_passengers=Count('invoices_train__passengers')
                ).filter(capacity__gte=F('num_passengers') + str(passengers))

        if new_data is None:
            return Response({'message': 'filter is empty',
                             'hint': 'you can send : starting_city - destination_city - passengers - departure_date - return_date'})
        elif not len(new_data):
            return Response({'message': 'Information matching the entries was not found'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            ser_data = TrainSerializer(instance=new_data, many=True)
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
