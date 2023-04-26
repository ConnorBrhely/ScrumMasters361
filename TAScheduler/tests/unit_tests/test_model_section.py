from TAScheduler.models import UserAccount, Course, Section
from django.test import TestCase
from django.db.utils import IntegrityError

class TestModelSection(TestCase):
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

    def test_add_ta(self):
        self.section.add_ta(self.account)
        self.assertEqual(self.section.tas.first(), self.account, msg="TA not added to section")
        non_ta_user = UserAccount.objects.register(
            email="teststudent@uwm.edu",
            password="TestPassword123!",
            first_name='Test',
            last_name='Student',
            user_type='STUDENT',
        )
        with self.assertRaises(ValueError, msg="Did not raise ValueError for non-TA user"):
            self.section.add_ta(non_ta_user)
        with self.assertRaises(ValueError, msg="Did not raise IntegrityError for input None"):
            self.section.add_ta(None)

    def test_remove_ta(self):
        self.section.tas.add(self.account)
        self.section.remove_ta(self.account)
        self.assertEqual(self.section.tas.count(), 0, msg="TA not removed from section")
        with self.assertRaises(ValueError, msg="Did not raise ValueError for input None"):
            self.section.remove_ta(None)