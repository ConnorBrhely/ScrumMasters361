from ..common import validate
from django.db import models
from TAScheduler.models import Section

class UserManager(models.Manager):
    def register(self, name, email, password, user_type, home_address=None, phone_number=None, office_hours=None):
        user = self.create(
            name=name,
            email=email,
            password=password,
            type=user_type,
            home_address=home_address,
            phone_number=phone_number,
            office_hours=office_hours
        )
        return user


class User(models.Model):
    class UserType(models.TextChoices):
        TA = 'TA', 'TA'
        PROFESSOR = 'PROFESSOR', 'Professor'
        ADMIN = 'ADMIN', 'Admin'

    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    type = models.CharField(max_length=32, choices=UserType.choices)
    home_address = models.CharField(max_length=256, null=True, blank=True)
    phone_number = models.CharField(max_length=16, null=True, blank=True)
    office_hours = models.CharField(max_length=256, null=True, blank=True)

    objects = UserManager()

    def update_contact_info(self, home_address: str = None, phone_number: str = None, office_hours: str = None):
        """
        Updates the contact information for a user
        :param home_address: The new home address for the user
        :param phone_number: The new phone number for the user
        :param office_hours: The new office hours for the user
        :return: The updated user object
        """
        self.home_address = home_address
        self.phone_number = phone_number
        self.office_hours = office_hours
        self.save()
        return self

    def update_password(self, password: str):
        """
        Updates the password for a user
        :param password: The new password for the user
        :return: The updated user object
        """
        if not validate.validate_password(password):
            raise ValueError('Password must be at least 8 characters long and contain at least one number and one uppercase letter')
        self.password = password
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
