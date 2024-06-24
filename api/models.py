from django.db import models
from django.utils import timezone

# Create your models here.
class RandomSession(models.Model):
    sessionID = models.CharField(max_length=2000)
    username = models.CharField(max_length=2000)
    status = models.CharField(max_length=50, null=True, blank=True)
    added = models.DateTimeField(default=timezone.now)