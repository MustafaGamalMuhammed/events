from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    def __str__(self):
        return self.email
    
    @property
    def name(self):
        return self.email.split('@')[0]