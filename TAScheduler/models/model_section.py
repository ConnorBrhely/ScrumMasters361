from django.db import models

class Section(models.Model):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    time = models.CharField(max_length=256)
    course = models.ForeignKey("TAScheduler.Course", on_delete=models.CASCADE, related_name='sections')
    tas = models.ManyToManyField("TAScheduler.User", related_name='sections')

    # Hello, world!
    def update_name(self, name: str):
        """
        Updates the name of a section
        :param name: The new name for the section
        :return: The updated section object
        """
        self.name = name
        self.save()
        return self

    def add_ta(self, user):
        """
        Adds a TA to a section
        :param user: The TA to add to the section
        :return: The updated section object
        """
        from TAScheduler.models import User
        if user.type != User.UserType.TA:
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
        self.tas.remove(user)
        self.save()
        return self