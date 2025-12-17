from rest_framework.generics import RetrieveUpdateDestroyAPIView , CreateAPIView , ListAPIView , GenericAPIView
from .models import UserProfile , PasswordReset
from .serializers import UserProfileSerializer, UserRegistrationSerializer , ResetPasswordRequestSerializer , ResetPasswordSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import PasswordReset
import os
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
            return UserProfile.objects.filter(user=user)

class UserProfileView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated , IsAdminUser]
    
    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)
    
    # def get_object(self):
    #     user = self.request.user
    #     if user.is_staff:
    #         return UserProfile.objects.all()
    #     else:
    #         return UserProfile.objects.filter(user=user)
    
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
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = UserProfile.objects.filter(email__iexact=email).first()
        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user) 

            reset_obj = PasswordReset(email=email, token=token)
            reset_obj.save()

            reset_url = f"{settings.PASSWORD_RESET_BASE_URL}/{token}"

            send_mail(
                subject='Password Reset Request',
                message=f'Hi {user.username},\nClick the link below to reset your password:\n{reset_url}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User with credentials not found"}, status=status.HTTP_404_NOT_FOUND)

class ResetPassword(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        new_password = data['new_password']
        confirm_password = data['confirm_password']
        
        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)
        
        reset_obj = PasswordReset.objects.filter(token=token).first()
        
        if not reset_obj:
            return Response({'error':'Invalid token'}, status=400)
        
        user = UserProfile.objects.filter(email=reset_obj.email).first()
        
        if user:
            user.set_password(request.data['new_password'])
            user.save()
            
            reset_obj.delete()
            
            return Response({'success':'Password updated'})
        else: 
            return Response({'error':'No user found'}, status=404)