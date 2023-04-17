from django.db import models

class User(models.Model):
    class UserType(models.TextChoices):
        STUDENT = 'TA', 'TA'
        PROFESSOR = 'PROFESSOR', 'Professor'
        ADMIN = 'ADMIN', 'Admin'

    name = models.CharField(max_length=128)
    email = models.EmailField()
    password = models.CharField(max_length=256)
    type = models.CharField(max_length=8, choices=UserType.choices)
    home_address = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=16)
    office_hours = models.CharField(max_length=256)


class Course(models.Model):
    name = models.CharField(max_length=128)
    term = models.CharField(max_length=128)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='instructor')


class Section(models.Model):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    time = models.CharField(max_length=256)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
