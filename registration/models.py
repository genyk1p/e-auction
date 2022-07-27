from django.db import models
import uuid


class TemporaryUser (models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    published = models.DateTimeField(auto_now_add=True, db_index=True)
    token = models.UUIDField(default=uuid.uuid4)
