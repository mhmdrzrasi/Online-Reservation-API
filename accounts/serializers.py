from rest_framework import serializers
import re

from .models import User


def check_phone_number(value):
    if not re.match(r'^09\d{9}$', value):
        raise serializers.ValidationError('Phone number should only be 11 digits and start with 09')


class UserRegisterSerializer(serializers.ModelSerializer):
    c_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'password', 'c_password')
        extra_kwargs = {
            'phone_number': {'validators': (check_phone_number,)},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        v_d = validated_data
        user = User.objects.create_user(
            email=v_d['email'],
            phone_number=v_d['phone_number'],
            password=v_d['password']
        )
        return user

    def validate(self, attrs):
        if attrs['password'] != attrs['c_password']:
            raise serializers.ValidationError('Password does not match confirm password')
        return attrs


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'last_login': {'write_only': True},
        }


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone_number', 'address', 'birthday')
