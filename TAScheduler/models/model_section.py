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

    def __str__(self):
        return f"{self.course} - {self.number}"