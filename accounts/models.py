from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class UserProfile(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False,primary_key=True)
    date_updated = models.DateTimeField(auto_now=True)
    email = models.EmailField(unique=True, blank=False, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
        
    def __str__(self):
        return self.username