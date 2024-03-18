from django.db import models
from django.utils import timezone
from account.models import Client
from blog.models import Blog


# Create your models here.
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    username = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    blogId = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.title
