from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=128)
    term = models.CharField(max_length=128)
    # String must be used instead of a foreign key to avoid circular imports
    instructor = models.ForeignKey("TAScheduler.UserAccount", null=True, on_delete=models.SET_NULL, related_name='instructor')
