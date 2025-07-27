from django.db import models

class YTVideo(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    