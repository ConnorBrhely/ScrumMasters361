from TAScheduler.models import UserAccount, Course, Section
from django.test import TestCase

class TestModelCourse(TestCase):
    def setUp(self):
        self.account = UserAccount.objects.register(
            email="testuser@uwm.edu",
            password="TestPassword123!",
            first_name='Test',
            last_name='User',
            user_type='TA',
        )

        self.course = Course.objects.create(
            name='Test Course',
            term='Fall 2023',
            instructor=self.account,
        )

        self.section = Section.objects.create(
            number='001',
            location='Test Location',
            time='Test Time',
            course=self.course,
        )