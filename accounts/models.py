from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    primary user model
    """
    email = models.EmailField(max_length=254, blank=True, null=True)
    fullname = models.CharField(max_length=550, blank=True, null=True)
    image_url = models.CharField(max_length=1000, default="https://png.pngtree.com/png-clipart/20190924/original/pngtree-user-vector-avatar-png-image_4830521.jpg")
    
    
    