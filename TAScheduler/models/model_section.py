from django.db import models
from TAScheduler.models import Course

class Section(models.Model):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    time = models.CharField(max_length=256)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    tas = models.ManyToManyField("TAScheduler.User", related_name='sections')
