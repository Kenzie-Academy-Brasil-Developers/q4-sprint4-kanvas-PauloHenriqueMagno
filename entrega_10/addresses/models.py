from audioop import maxpp
from uuid import uuid4
from django.db import models

class Addresses(models.Model):
    uuid = models.UUIDField(primary_key = True, default = uuid4, editable = False)
    street = models.CharField(max_length = 250)
    house_number = models.IntegerField()
    city = models.CharField(max_length = 200)
    state = models.CharField(max_length = 200)
    zip_code = models.CharField(max_length = 15)
    country = models.CharField(max_length = 60)