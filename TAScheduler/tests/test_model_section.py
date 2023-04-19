from TAScheduler.models import User, Course, Section
from django.test import TestCase

class TestModelUser(TestCase):
    def setUp(self):
            self.user = User.objects.create(
                name='Test User',
                type='INSTRUCTOR',
            )

            self.course = Course.objects.create(
                name='Test Course',
                term='Fall 2023',
                instructor=self.user,
            )

            self.section = Section.objects.create(
                name='Test Section',
                location='Test Location',
                time='Test Time',
                course=self.course,
            )

        #TODO: Add tests for Section model

    def testSection(self):
        self.assertequal(self.section.name, 'Test Section' , 'name is not the same as section')

    def testLocation(self):
        self.assertequal(self.section.location, 'Test Location', 'location does not match given data')

    def testTime(self):
        self.assertequal