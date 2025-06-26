from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .serializers import CustomRegisterSerializer, UserUpdateSerializer, LoginSerializer
from .models import CustomUser 


class RegisterView(APIView):
    def post(self, request):
        serializer = CustomRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(serializer.validated_data)  # ← düzeltme burada

            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Kayıt başarılı.",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone_number": user.phone_number,
                "profile_picture": request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'email': user.email, 
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'profile_picture': request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None,
        }, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserUpdateSerializer(request.user, context={'request': request}) 
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({'detail': 'Kullanıcı hesabı başarıyla silindi.'}, status=status.HTTP_204_NO_CONTENT)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.data)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return Response({"detail": "Şifre başarıyla değiştirildi."}, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)