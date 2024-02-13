from django.db import models
from django.utils import timezone
from account.models import Client


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    data_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
