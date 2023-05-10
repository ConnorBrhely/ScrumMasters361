from django.db import models
from ..common import validate

class Section(models.Model):
    number = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    time = models.CharField(max_length=256)
    course = models.ForeignKey("TAScheduler.Course", on_delete=models.CASCADE, related_name='sections', null=True, blank=True)
    tas = models.ManyToManyField("TAScheduler.UserAccount", related_name='sections')

    def update_number(self, number: str):
        """
        Updates the name of a section
        :param number: The new name for the section
        :return: The updated section object
        """
        if number is None:
            raise ValueError("Name cannot be blank")
        if number.strip() == "":
            raise ValueError("Name cannot be blank")
        if not validate.validate_section_number(number):
            raise ValueError("Invalid section number")
        self.number = number
        self.save()
        return self

    def add_ta(self, user):
        """
        Adds a TA to a section
        :param user: The TA to add to the section
        :return: The updated section object
        """
        if user is None:
            raise ValueError("User cannot be blank")

        from TAScheduler.models import UserAccount
        if user.type != UserAccount.UserType.TA:
            raise ValueError('User must be a TA to be added to a section')

        self.tas.add(user)
        self.save()
        return self

    def remove_ta(self, user):
        """
        Removes a TA from a section
        :param user: The TA to remove from the section
        :return: The updated section object
        """
        if user is None:
            raise ValueError("User cannot be blank")
        self.tas.remove(user)
        self.save()
        return self



    def update_location(self, location: str):
        """
        Updates the location of the section
        :param location: The new location of the section
        :return: The updated section object
        """
        if location is None:
            raise ValueError("Location cannot be blank")
        if location.strip() == "":
            raise ValueError("Location cannot be blank")
        self.location = location
        self.save()
        return self

    def update_time(self, time: str):
        """
        Updates the time of the section
        :param time: The new time of the section
        :return: The updated section object
        """
        if time is None:
            raise ValueError("Time cannot be blank")
        if time.strip() == "":
            raise ValueError("Time cannot be blank")
        self.time = time
        self.save()
        return self

    def remove_all_tas(self):
        """
        Removes all TAs from the section
        :return: The updated section object
        """
        self.tas.clear()
        self.save()
        return self

    def is_ta_assigned(self, user):
        """
        Checks if a TA is assigned to the section
        :param user: The user to check
        :return: True if the user is a TA and assigned to the section, False otherwise
        """
        if user is None:
            raise ValueError("User cannot be blank")
        return user in self.tas.all()

    def is_full(self):
        """
        Checks if the section is at full capacity
        :return: True if the section is full, False otherwise
        """
        return self.tas.count() >= self.course.max_tas_per_section


    def __str__(self):
        return f"{self.course} - {self.number}"