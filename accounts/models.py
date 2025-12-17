from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class UserProfile(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False,primary_key=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('username', 'email')
        
    def __str__(self):
        return self.username
    
class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        unique_together = ('email', 'token')