from TAScheduler.models import UserAccount, Course, Section
from django.test import TestCase


class TestModelUser(TestCase):
    def setUp(self):
        self.account = UserAccount.objects.register(
            email="testuser@uwm.edu",
            password="TestPassword123!",
            first_name='Test',
            last_name='User',
            user_type='INSTRUCTOR',
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

    def test_update_address(self):
        self.account.update_address('1234 S. Street')
        self.assertEqual('1234 S. Street', self.account.home_address,
                         msg='Home address not updated when valid address entered')
        with self.assertRaises(ValueError, msg='ValueError not thrown when blank input entered'):
            self.account.update_address('')
        with self.assertRaises(ValueError, msg='ValueError not thrown when blank input with whitespace entered'):
            self.account.update_address('   \t\n')

    def test_update_phone_number(self):
        self.account.update_phone_number('(414) 444-4444')
        self.assertEqual('(414) 444-4444', self.account.phone_number,
                         msg='Phone number not updated when valid phone number entered')
        with self.assertRaises(ValueError, msg='ValueError not thrown when extra characters entered'):
            self.account.update_phone_number('(414) 555-12/34')
        with self.assertRaises(ValueError, msg='ValueError not thrown when blank input entered'):
            self.account.update_phone_number('')
        with self.assertRaises(ValueError, msg='ValueError not thrown when blank input with whitespace entered'):
            self.account.update_phone_number('   \t\n')

    def test_update_office_hours(self):
        self.account.update_office_hours('MWF 8-9')
        self.assertEqual('MWF 8-9', self.account.office_hours,
                         msg='Office hours not updated when valid office hours entered')

    def test_update_no_hours(self):
        with self.assertRaises(ValueError, msg='ValueError not thrown when blank input entered'):
            self.account.update_office_hours('')

    def test_update_only_spaces(self):
        with self.assertRaises(ValueError, msg='ValueError not thrown when blank input with whitespace entered'):
            self.account.update_office_hours('   \t\n')

    def test_add_to_section(self):
        self.account.add_to_section(self.section)
        self.assertEqual(self.section.tas.count(), 1,
                         msg='Section not added to user when valid section entered')

    def test_check_TA(self):
        added_ta = self.section.tas.first()
        ta_name = added_ta.first_name + ' ' + added_ta.last_name
        expected_ta_name = self.account.first_name + ' ' + self.account.last_name
        self.assertEqual(ta_name, expected_ta_name,
                         msg='Section not added to user when valid section entered')

    def test_no_TA(self):
        with self.assertRaises(ValueError, msg='ValueError not thrown when None entered'):
            self.account.add_to_section(None)

    def test_remove_TA(self):
        self.section.remove_ta(self.account)
        self.assertEqual(0, self.section.tas.count(), msg = 'Section did not remove TA')

    #def test_remove_no_TA(self):


    def test_set_password(self):
        old_hash = self.account.user.password
        self.account.update_password("Password123!")
        self.assertNotEqual(self.account.user.password, old_hash, msg="Password not updated when valid password entered")

        with self.assertRaises(ValueError, msg="ValueError not thrown when password is < 8 characters"):
            self.account.update_password("Error1!")
        with self.assertRaises(ValueError, msg="ValueError not thrown when password has no number"):
            self.account.update_password("Password!")
        with self.assertRaises(ValueError, msg="ValueError not thrown when password has no special character"):
            self.account.update_password("Password123")
        with self.assertRaises(ValueError, msg="ValueError not thrown when password has no uppercase character"):
            self.account.update_password("password123!")
        with self.assertRaises(ValueError, msg="Value error not thrown when blank input entered"):
            self.account.update_password("")

    def test_changeValidPhone(self):
        self.account.update_phone_number("4144444444")
        self.assertEqual(self.account.phone_number, "4144444444", msg="Phone number not updated with valid number")

    def test_invalidPhone(self):
        with self.assertRaises(ValueError, msg="ValueError not thrown when phone number is too short"):
            self.account.update_phone_number("414444444")

    def test_blankPhone(self):
        with self.assertRaises(ValueError, msg="ValueError not thrown when blank number entered"):
            self.account.update_phone_number("")

    def test_invalidCharsPhone(self):
        with self.assertRaises(ValueError, msg="ValueError not thrown when invalid character entered"):
            self.account.update_phone_number("414B44[as")

    def test_blankAddress(self):
        with self.assertRaises(ValueError, msg="ValueError not thrown when blank address entered"):
            self.account.update_address("")

    def test_validAddress(self):
        self.account.update_address("123 S Fake St")
        self.assertEqual(self.account.home_address, "123 S Fake St")




