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
    instructor = models.ForeignKey("TAScheduler.UserAccount", null=True, on_delete=models.SET_NULL, related_name='instructor')
    # String must be used instead of an import reference to avoid circular imports
    # instructors = models.ManyToManyField("TAScheduler.UserAccount", related_name='courses')

    # def add_instructor(self, user):    #     adds instructor
    #     from TAScheduler.models import UserAccount
    #     if user.type != UserAccount.UserType.INSTRUCTOR:
    #         raise ValueError('User must be an instructor to be added to a course')
    #     self.tas.add(user)
    #     self.save()
    #     return self
    #
    # def remove_instructor(self,user):
    #     self.tas.remove(user)
    #     self.save()

    def get_instructor(self):
        return self.instructor

    def update_name(self,name):
        self.name = name
        self.save()

    def update_number(self,number):
        self.number = number
        self.save()

    def update_term_year(self,year):
        self.term_year = year
        self.save()

    def update_term_season(self,season):
        self.term_season = season
        self.save()

    def update_instructor(self,user=None):
        self.instructor = user
        self.save()

    def __str__(self):
        return f"{self.name} ({self.number}), {self.term_season} {self.term_year} | " \
               f"{self.instructor.first_name} {self.instructor.last_name}"