from django.urls import path
from .views import (
    ListUserProfileView,
    UserProfileView,
    UserRegistrationView,
    LoginView,
    LogoutView,
    RequestPasswordReset,
    ResetPassword,
)

urlpatterns = [
    # Users
    path('users/', ListUserProfileView.as_view(), name='list-users'),             
    path('users/me/', UserProfileView.as_view(), name='user-profile'),            
    path('users/register/', UserRegistrationView.as_view(), name='user-register'),

    # Authentication
    path('login/', LoginView.as_view(), name='login'),                             
    path('logout/', LogoutView.as_view(), name='logout'),                          

    # Password Reset
    path('password-reset/request/', RequestPasswordReset.as_view(), name='password-reset-request'),   
    path('password-reset/<str:token>/', ResetPassword.as_view(), name='password-reset'),           
]
