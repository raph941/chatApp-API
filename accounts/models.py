from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    primary user model
    """
    email = models.EmailField(max_length=254, blank=True, null=True)
    fullname = models.CharField(max_length=550, blank=True, null=True)
    
    @property
    def initials(self):
        init_name = ''
        try:
            fullname = self.fullname
            username = self.username
            names = fullname.split() if fullname != None else username.split()
            for name in names: init_name += name[0]            
            return init_name.upper()
        except: return init_name
    