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

