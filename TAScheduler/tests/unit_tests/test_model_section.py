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
            term_season='Fall',
            term_year=2023,
            instructor=self.account,
        )

        self.section = Section.objects.create(
            number='001',
            location='Test Location',
            time='Test Time',
            course=self.course,
        )

    def test_update_number(self):
        self.section.update_number("001")
        self.assertEqual(self.section.number, "001", msg="Section name not updated")
        with self.assertRaises(ValueError, msg="Did not raise ValueError for invalid characters"):
            self.section.update_number("Invalid Section Method") # Only digits and '-' allowed
        with self.assertRaises(ValueError, msg="Did not raise IntegrityError for input None"):
            self.section.update_number(None)
        with self.assertRaises(ValueError, msg="Did not raise ValueError for blank input"):
            self.section.update_number('')
        with self.assertRaises(ValueError, msg="Did not raise ValueError for whitespace input"):
            self.section.update_number('   \t\n')

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


    def test_section_str(self):
        self.assertEqual(str(self.section), f"{self.course} - {self.section.number}")
