from ..common import validate
from django.db import models
from django.contrib.auth.models import User
from TAScheduler.models import Section

class UserAccountManager(models.Manager):
    def register(self, first_name, last_name, email, password, user_type, home_address=None, phone_number=None, office_hours=None):
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
        )
        user.save()
        user_account = self.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            type=user_type,
            home_address=home_address,
            phone_number=phone_number,
            office_hours=office_hours,
        )
        return user_account


class UserAccount(models.Model):
    class UserType(models.TextChoices):
        TA = 'TA', 'TA'
        PROFESSOR = 'PROFESSOR', 'Professor'
        ADMIN = 'ADMIN', 'Admin'

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    type = models.CharField(max_length=32, choices=UserType.choices)
    home_address = models.CharField(max_length=256, null=True, blank=True)
    phone_number = models.CharField(max_length=16, null=True, blank=True)
    office_hours = models.CharField(max_length=256, null=True, blank=True)

    objects = UserAccountManager()

    def update_address(self, home_address: str = None):
        """
        Updates the home address for a user
        :param home_address: The new home address for the user
        :return: The updated user object
        """
        self.home_address = home_address
        self.save()
        return self

    def update_phone_number(self, phone_number: str = None):
        """
        Updates the phone number for a user
        :param phone_number: The new phone number for the user
        :return: The updated user object
        """
        self.phone_number = phone_number
        self.save()
        return self

    def update_office_hours(self, office_hours: str = None):
        """
        Updates the office hours for a user
        :param office_hours: The new office hours for the user
        :return: The updated user object
        """
        self.office_hours = office_hours
        self.save()
        return self

    def add_to_section(self, section: Section):
        """
        Adds a user to a section
        :param section: The section to add the user to
        :return: The updated user object
        """
        section.tas.add(self)
        section.save()
        return self
