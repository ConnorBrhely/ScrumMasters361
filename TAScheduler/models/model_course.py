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

    def add_instructor(self, user):
        from TAScheduler.models import UserAccount
        if user.type != UserAccount.UserType.TA:
            raise ValueError('User must be a instructor')
        self.instructor.add(user)
        self.save()
        return self

    def update_name(self, name):
        self.name = name
        self.save()
        return self

    def set_term(self, term_season, term_year):
        self.term_season = term_season
        self.term_year = term_year
        self.save()
        return self