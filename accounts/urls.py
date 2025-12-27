from django.urls import path
from .views import (
    ListUserProfileView,
    UserProfileView,
    UserRegistrationView,
    LoginView,
    LogoutView,
    RequestPasswordReset,
    ResetPassword,
    ChangePasswordView
)

urlpatterns = [
    # Users
    path('users/', ListUserProfileView.as_view(), name='list-users'),             
    path('users/me/', UserProfileView.as_view(), name='user-profile'),            
    path('users/<uuid:user_id>/', UserProfileView.as_view(), name='user-profile'),            
    path('users/register/', UserRegistrationView.as_view(), name='user-register'),

    path('login/', LoginView.as_view(), name='login'),                             
    path('logout/', LogoutView.as_view(), name='logout'),                          

    path('password-reset/request/', RequestPasswordReset.as_view(), name='password-reset-request'),
    path('password-reset/<uidb64>/<token>/', ResetPassword.as_view(), name='password-reset-confirm'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]