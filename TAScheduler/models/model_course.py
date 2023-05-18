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
    # String must be used instead of a foreign key to avoid circular imports
    instructor = models.ForeignKey("TAScheduler.UserAccount", null=True, on_delete=models.SET_NULL, related_name='instructor')

    def add_instructor(self, user):    #     adds instructor
        from TAScheduler.models import UserAccount
        if user.type != UserAccount.UserType.instructor:
            raise ValueError('User must be an instructor to be added to a course')
        self.tas.add(user)
        self.save()
        return self

    def remove_instructor(self,user):
        self.tas.remove(user)
        self.save()

    def get_instructor(self):
        return self.instructor

    def update_name(self,name):
        self.name = name

    def update_number(self,number):
        self.number = number

    def update_term_year(self,year):
        self.term_year = year

    def update_term_season(self,season):
        self.term_season = season

    def update_instructor(self,user):
        self.instructor = user

    def __str__(self):
        return f"{self.name} ({self.number}), {self.term_season} {self.term_year} | " \
               f"{self.instructor.first_name} {self.instructor.last_name}"