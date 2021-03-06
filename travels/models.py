from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def serialize(self):
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "id": self.id,           
        }
