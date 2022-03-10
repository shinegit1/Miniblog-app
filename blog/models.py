from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
  title =models.CharField(max_length=200)
  descript =models.TextField()

class Contact(User):
  subject =models.CharField(max_length=200)
  message =models.TextField()
