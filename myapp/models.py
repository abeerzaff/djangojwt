
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)  # Override this!
    email = models.EmailField(unique=True)  # Make email required and unique

    USERNAME_FIELD = 'email'         # Use email to log in
    REQUIRED_FIELDS = ['username'] 

#    class Meta:
#        constraints = []
#        indexes = []
#        unique_together = []  # override default behavior to remove uniqueness from username
