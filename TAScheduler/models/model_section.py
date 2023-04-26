from django.db import models

class Section(models.Model):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    time = models.CharField(max_length=256)
    course = models.ForeignKey("TAScheduler.Course", on_delete=models.CASCADE, related_name='sections', null=True, blank=True)
    tas = models.ManyToManyField("TAScheduler.UserAccount", related_name='sections', null=True, blank=True)

    def update_name(self, name: str):
        """
        Updates the name of a section
        :param name: The new name for the section
        :return: The updated section object
        """
        if name is None:
            raise ValueError("Name cannot be blank")
        if name.strip() == "":
            raise ValueError("Name cannot be blank")
        self.name = name
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