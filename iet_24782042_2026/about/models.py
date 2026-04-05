from django.db import models

class Report(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False) 
