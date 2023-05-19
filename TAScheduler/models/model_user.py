from django.db.models import QuerySet

from ..common import validate
from django.db import models
from django.contrib.auth.models import User
from TAScheduler.models import Section, Course

class UserAccountManager(models.Manager):
    def register(self, first_name, last_name, email, password, user_type, home_address=None, phone_number=None, office_hours=None):
        """
        Creates a new user account and saves it to the database
        :param first_name: The first name of the user
        :param last_name: The last name of the user
        :param email: The email of the user
        :param password: The password of the user
        :param user_type: The type of user
        :param home_address: The home address of the user
        :param phone_number: The phone number of the user
        :param office_hours: The office hours of the user
        :return: The newly created user account
        """
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
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
        user_account.save()
        return user_account


class UserAccount(models.Model):
    class UserType(models.TextChoices):
        TA = 'TA', 'TA'
        INSTRUCTOR = 'INSTRUCTOR', 'Instructor'
        ADMIN = 'ADMIN', 'Admin'

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    type = models.CharField(max_length=32, choices=UserType.choices)
    home_address = models.CharField(max_length=256, null=True, blank=True)
    phone_number = models.CharField(max_length=16, null=True, blank=True)
    office_hours = models.CharField(max_length=256, null=True, blank=True)

    objects = UserAccountManager()

    def update_name(self, first_name: str, last_name: str):
        """
        Updates the name for a user
        :param first_name:
        :param last_name:
        :return:
        """
        if not validate.name(first_name, last_name):
            raise ValueError("Name failed validation")
        self.first_name = first_name
        self.last_name = last_name
        self.save()
        return self

    def update_email(self, email: str):
        """
        Updates the email for a user
        :param email: The new email for the user
        :return: The updated user object
        """
        if email is None:
            raise ValueError("Email cannot be blank")
        if email.strip() == "":
            raise ValueError("Email cannot be blank")
        if not validate.email(email):
            raise ValueError("Invalid email")
        self.user.username = email
        self.user.email = email
        self.user.save()
        return self

    def update_password(self, password: str = None):
        """
        Updates the password for a user
        :param password: The new password for the user
        :return: The updated user object
        """
        if password is None:
            raise ValueError("Password cannot be blank")
        if password.strip() == "":
            raise ValueError("Password cannot be blank")
        if not validate.password(password):
            raise ValueError("Invalid password")
        self.user.set_password(password)
        self.user.save()
        return self

    def update_address(self, home_address: str = None):
        """
        Updates the home address for a user
        :param home_address: The new home address for the user
        :return: The updated user object
        """
        if home_address is None:
            raise ValueError("Home address cannot be blank")
        if home_address.strip() == "":
            raise ValueError("Home address cannot be blank")
        self.home_address = home_address
        self.save()
        return self

    def update_phone_number(self, phone_number: str = None):
        """
        Updates the phone number for a user
        :param phone_number: The new phone number for the user
        :return: The updated user object
        """
        if phone_number is None:
            raise ValueError("Phone number cannot be blank")
        if not validate.phone_number(phone_number):
            raise ValueError("Invalid phone number")
        self.phone_number = phone_number
        self.save()
        return self

    def update_office_hours(self, office_hours: str = None):
        """
        Updates the office hours for a user
        :param office_hours: The new office hours for the user
        :return: The updated user object
        """
        if office_hours is None:
            raise ValueError("Office hours cannot be blank")
        if office_hours.strip() == "":
            raise ValueError("Office hours cannot be blank")
        self.office_hours = office_hours
        self.save()
        return self

    def add_to_section(self, section: Section):
        """
        Adds a user to a section
        :param section: The section to add the user to
        :return: The updated user object
        """
        if section is None:
            raise ValueError("Section cannot be blank")
        section.tas.add(self)
        section.save()
        return self

    def get_courses(self) -> QuerySet[Course]:
        if self.type == self.UserType.TA:
            # Get all sections that the user is a TA for
            sections = Section.objects.all()
            courses = []
            for section in sections:
                if self in section.tas.all():
                    courses.append(section.course)

            # Must convert to a QuerySet for filtering to work, sorry!
            queryset = QuerySet(model=Course, query=None)
            queryset._result_cache = {i: None for i in courses}
            queryset._prefetch_done = True
            return queryset
        elif self.type == self.UserType.INSTRUCTOR:
            return Course.objects.filter(instructor=self)
        else:
            return Course.objects.all()