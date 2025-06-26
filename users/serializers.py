# users/serializers.py

from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import transaction


# JWT Token payload'ını özelleştiren serializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        return token


# Kayıt Serializer'ı
class CustomRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = PhoneNumberField(required=False, allow_null=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password2": "Şifreler eşleşmiyor!"})
        return data

    @transaction.atomic
    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', None),
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user


# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError("Girdiğiniz e-posta veya şifre hatalı.", code='authorization')
        else:
            raise serializers.ValidationError('"Email" ve "Şifre" alanları gereklidir.', code='authorization')
        data['user'] = user
        return data


# Kullanıcı Bilgilerini Güncelleme Serializer'ı
class UserUpdateSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(required=False, allow_null=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'profile_picture', 'phone_number']
        read_only_fields = ['email']

    def validate_email(self, value):
        user = self.context['request'].user
        if CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Bu e-posta adresi zaten kullanılıyor.")
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        if 'profile_picture' in validated_data:
            instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.save()
        return instance
