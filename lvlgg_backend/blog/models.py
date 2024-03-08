from django.db import models
from django.utils import timezone
from account.models import Client


# Create your models here.
class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    likes = models.IntegerField(default=0) 
    dislikes = models.IntegerField(default=0)  
    game = models.TextField(default="null")  
    def __str__(self):
        return self.title
