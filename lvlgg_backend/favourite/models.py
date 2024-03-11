from account.models import Client
from blog.models import Blog
from django.db import models


# Create your models here.
class Favourite(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
