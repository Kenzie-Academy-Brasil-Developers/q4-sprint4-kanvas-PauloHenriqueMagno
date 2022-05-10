from uuid import uuid4
from django.db import models

class Courses(models.Model):
    uuid = models.UUIDField(primary_key = True, default = uuid4, editable = False)
    name = models.CharField(max_length = 150, unique = True)
    demo_time = models.TimeField()
    created_at = models.DateTimeField()
    link_repo = models.CharField(max_length = 250)

    instructor = models.ForeignKey('users.Users', on_delete = models.SET_NULL, related_name = 'course', null = True)

    students = models.ManyToManyField('users.Users', related_name = 'courses')