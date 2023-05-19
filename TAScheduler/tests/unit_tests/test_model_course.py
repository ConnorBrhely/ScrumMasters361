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
        with self.assertRaises(ValueError, msg="Course Name must not be empty"):
            self.course.update_name("")

    def test_update_name_whitespace(self):
      with self.assertRaises(ValueError, msg="Course Name did not raise ValueError for only whitespace"):
        self.course.update_name("   \t\n")

    def test_update_number(self):
        self.course.update_number("123")
        self.assertEqual(self.course.number, "123", msg="Course Number not updated")

    def test_update_no_number(self):
        with self.assertRaises(ValueError, msg="Course Number must not be empty"):
            self.course.update_number("")

    def test_update_invalid_number(self):
        with self.assertRaises(ValueError, msg="Course Number must contain numbers"):
            self.course.update_number("abcd")

    def test_update_number_whitespace(self):
        with self.assertRaises(ValueError, msg="Course Number did not raise ValueError for only whitespace"):
            self.course.update_number("   \t\n")

    def test_update_term_year(self):
        self.course.update_term_year("2025")
        self.assertEqual(self.course.term_year, "2025", msg="Term Year not updated")
    
    def test_str(self):
        expected_str = 'Test Course (001), Fall 2023 | Test User'
        self.assertEqual(str(self.course), expected_str)

    def test_empty_term_year(self):
        with self.assertRaises(ValueError, msg="Course Term must not be None"):
            self.course.update_term_year(None)

    def test_update_invalid_term_year(self):
        with self.assertRaises(ValueError, msg="Course Term must contain numbers"):
            self.course.update_number("abcd")

    def test_update_number_whitespace(self):
        with self.assertRaises(ValueError, msg="Course Term did not raise ValueError for only whitespace"):
            self.course.update_term_year("   \t\n")
