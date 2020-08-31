from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Save(models.Model):
  title = models.CharField(max_length=150)
  post_id = models.CharField(max_length=150)
  img_url = models.CharField(max_length=150)
  category = models.CharField(max_length=10)
  author = models.CharField(max_length=150)
  post_date = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(User, on_delete = models.CASCADE)
  