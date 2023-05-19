from django.db import models
from ..common import validate

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
    # String must be used instead of an import reference to avoid circular imports
    instructor = models.ForeignKey("TAScheduler.UserAccount", null=True, on_delete=models.SET_NULL, related_name='instructor')

    def get_instructor(self):
        return self.instructor

    def update_name(self, name: str):
        if len(name.strip()) == 0:
            raise ValueError("Name cannot be blank")
        self.name = name
        self.save()

    def update_number(self,number):
        if validate.course_number(number) is False:
            raise ValueError("Invalid course number")
        self.number = number
        self.save()

    def update_term_year(self,year):
        if validate.year(year) is False:
            raise ValueError("Invalid year")
        self.term_year = year
        self.save()

    def update_term_season(self,season):
        self.term_season = season
        self.save()

    def update_instructor(self,user=None):
        self.instructor = user
        self.save()

    def __str__(self):
        # If instructor is None, display "No Instructor" instead of "None"
        if self.instructor is None:
            return f"{self.name} ({self.number}), {self.term_season} {self.term_year} | No Instructor"
        return f"{self.name} ({self.number}), {self.term_season} {self.term_year} | " \
               f"{self.instructor.first_name} {self.instructor.last_name}"