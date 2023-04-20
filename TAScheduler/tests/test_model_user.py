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

    def test_updateHomeAddress(self):
        self.user.home_address = '1234 S. Street'
        self.save()
        self.assertEqual('1234 S. Street', self.user.home_address, msg='user home address updated')

    def test_noHomeAddress(self):
        self.user.home_address = ''
        self.save()
        self.assertEqual('', self.user.home_address, msg='user has no home address')

    def test_updatePhoneNumber(self):
        self.user.phone_number = '(414) 444-4444'
        self.save()
        self.assertEqual('(414) 444-4444', self.user.phone_number, msg='user has updated phone number')

    def test_updateOfficeHours(self):
        self.user.office_hours = '2-4 pm MW'
        self.save()
        self.assertEqual('2-4 pm MW', self.user.office_hours, msg='user has updated office hours')

    def test_noOfficeHours(self):
        self.user.office_hours = ''
        self.save()
        self.assertEqual('', self.user.office_hours, msg='user has no office hours')

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