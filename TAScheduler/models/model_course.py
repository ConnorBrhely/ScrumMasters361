from django.db import models

class Course(models.Model):
    TERM_SEASON_CHOICES = [
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
    ]
    name = models.CharField(max_length=128)
    number = models.CharField(max_length=128)
    term_year = models.CharField(max_length=4)
    term_season = models.CharField(max_length=6, choices=TERM_SEASON_CHOICES)
    # String must be used instead of a foreign key to avoid circular imports
    instructor = models.ForeignKey("TAScheduler.UserAccount", null=True, on_delete=models.SET_NULL, related_name='instructor')
