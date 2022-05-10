from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    uuid = models.UUIDField(primary_key = True, default = uuid4, editable = False)
    email = models.CharField(max_length = 150, unique = True, null = False)
    is_admin = models.BooleanField(default = False, editable = False)
    first_name = models.CharField(max_length = 150)
    last_name = models.CharField(max_length = 150)
    # password
    username = models.CharField(max_length = 150, null = True)

    address = models.ForeignKey('addresses.Addresses', on_delete = models.SET_NULL, related_name = 'users', null = True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []