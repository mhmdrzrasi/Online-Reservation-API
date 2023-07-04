from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .serializers import UserRegisterSerializer, UserViewSerializer, UserUpdateSerializer
from .models import User


class UserRegisterView(APIView):

    def post(self, request: Request):
        ser_data = UserRegisterSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(data=ser_data.data, status=status.HTTP_201_CREATED)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserGetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        user = self.request.user
        ser_data = UserViewSerializer(instance=user)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request: Request):
        user = self.request.user
        ser_data = UserUpdateSerializer(instance=user, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: Request):
        user = self.request.user
        user.delete()
        return Response({'message': 'user deleted successfully'})

