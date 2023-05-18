from TAScheduler.models import UserAccount, Course, Section
from django.test import TestCase

class TestModelCourse(TestCase):
    def setUp(self):
        self.account = UserAccount.objects.register(
            email="testuser@uwm.edu",
            password="TestPassword123!",
            first_name='Test',
            last_name='User',
            user_type=UserAccount.UserType.TA,
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

    def test_update_name(self):
        self.course.update_name("hello")
        self.assertEqual(self.course.name, "hello", msg="Course name not updated")
    def test_update_no_name(self):
        self.course.update_name("")
        self.assertRaises(ValueError, msg="Course Name must not be empty")

    def test_update_invalid_name(self):
        self.course.update_name("111")
        self.assertRaises(ValueError, msg="Course Name must contain letters")

    def test_update_name_whitespace(self):
      self.course.update_name("   \t\n")
      self.assertRaises(ValueError, msg="Course Name did not raise ValueError for only whitespace")


    def test_update_number(self):
        self.course.update_number("123")
        self.assertEqual(self.course.number, "hello", msg="Course Number not updated")
    def test_update_no_number(self):
        self.course.update_number("")
        self.assertRaises(ValueError, msg="Course Number must not be empty")

    def test_update_invalid_number(self):
        self.course.update_number("abcd")
        self.assertRaises(ValueError, msg="Course Number must contain numbers")

    def test_update_number_whitespace(self):
       self.course.update_number("   \t\n")
       self.assertRaises(ValueError, msg="Course Number did not raise ValueError for only whitespace")


    def test_update_term_year(self):
        self.course.update_term_year("2025")
        self.assertEqual(self.course.term_year, "2025", msg="Term Year not updated")

    def test_empty_term_year(self):
        self.course.update_term_year(None)
        self.assertRaises(ValueError, msg="Course Term must not be None")



    def test_update_invalid_term_year(self):
        self.course.update_number("abcd")
        self.assertRaises(ValueError, msg="Course Term must contain numbers")

    def test_update_number_whitespace(self):
        self.course.update_term_year("   \t\n")
        self.assertRaises(ValueError, msg="Course Term did not raise ValueError for only whitespace")
