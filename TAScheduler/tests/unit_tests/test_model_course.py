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
            name='Test Section',
            location='Test Location',
            time='Test Time',
            course=self.course,
        )

    def test_update_name(self):
        self.section.update_name("New Section Method")
        self.assertEqual(self.section.name, "New Section Method", msg="Section name not updated")
        with self.assertRaises(ValueError, msg="Did not raise IntegrityError for input None"):
            self.section.update_name(None)
        with self.assertRaises(ValueError, msg="Did not raise ValueError for blank input"):
            self.section.update_name('')
        with self.assertRaises(ValueError, msg="Did not raise ValueError for whitespace input"):
            self.section.update_name('   \t\n')