from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    descript = models.TextField()

    def __str__(self):
        return self.title


class Contact(User):
    subject = models.CharField(max_length=200)
    message = models.TextField()
