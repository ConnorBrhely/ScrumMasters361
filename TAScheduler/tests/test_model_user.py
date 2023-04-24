from TAScheduler.models import User, Course, Section
from django.test import TestCase


class TestModelUser(TestCase):
    def setUp(self):
            self.user = UserAccount.objects.register(
                first_name='Test',
                last_name='User',
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

    def test_updatepassword(self):
        self.user.update_password("Password123")
        self.assertEqual(self.user.password, "Password123", msg="Password not updated when valid password entered")
        with self.assertRaises(ValueError, msg="Value error not thrown when password is not 8 characters"):
            self.user.update_password("error1")
        with self.assertRaises(ValueError, msg="Value error not thrown when password is 8 characters without number"):
            self.user.update_password("Password")
        with self.assertRaises(ValueError,
                               msg="Value error not thrown when password is 8 characters long with number but no "
                                   "uppercase letter"):
            self.user.update_password("password123")
        with self.assertRaises(ValueError, msg="Value error not thrown when blank input entered"):
            self.user.update_password("")

    def test_updateContactInfo(self):
        self.user.update_contact_info(self, '1234 S. Street', '(414) 444-4444', '2-4 pm MW')
        self.save()
        self.assertEqual('1234 S. Street', self.user.home_address, msg='user home address updated')
        self.assertEqual('(414) 444-4444', self.user.phone_number, msg='user phone number updated')
        self.assertEqual('2-4 pm MW', self.user.office_hours, msg='office hours updated')

    def test_noContactInfo(self):
        self.user.update_contact_info(self, '', '', '')
        self.save()
        self.assertEqual('', self.user.home_address, msg='user has no home address')
        self.assertEqual('', self.user.phone_number, msg='user has no phone number')
        self.assertEqual('', self.user.office_hours, msg='user has no office hours')