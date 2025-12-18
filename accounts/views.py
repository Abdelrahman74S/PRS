from rest_framework.generics import RetrieveUpdateDestroyAPIView , CreateAPIView , ListAPIView , GenericAPIView
from .models import UserProfile 
from .serializers import UserProfileSerializer, UserRegistrationSerializer , ResetPasswordRequestSerializer , ResetPasswordSerializer
import os
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny , IsAuthenticated , IsAdminUser
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class ListUserProfileView(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return UserProfile.objects.all()
        else:
            return UserProfile.objects.filter(pk=user.pk)

class UserProfileView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg  = 'user_id'
    
    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or 'pk'
        user_id = self.kwargs.get(lookup_url_kwarg)

        if user_id:
            if self.request.user.is_staff:
                return get_object_or_404(UserProfile, pk=user_id)
            else:
                return self.request.user 
        
        return self.request.user
    

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        } 
        
        response_data = {
            'user': serializer.data,
            'tokens': tokens,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    
class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = [AllowAny]
    
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
class RequestPasswordReset(GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = User.objects.filter(email__iexact=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            reset_url = f"{settings.PASSWORD_RESET_BASE_URL}/{uidb64}/{token}/"

            send_mail(
                subject='Password Reset Request',
                message=f'Hi {user.username},\nClick here to reset: \n{reset_url}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class ResetPassword(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def post(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            
            token_generator = PasswordResetTokenGenerator()
            
            if not token_generator.check_token(user, token):
                return Response({'error': 'Token is invalid or expired'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({'success': 'Password updated successfully'}, status=status.HTTP_200_OK)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid token or user ID'}, status=status.HTTP_400_BAD_REQUEST)