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
            number='001',
            location='Test Location',
            time='Test Time',
            course=self.course,
        )
    def test_course_name(self):
        self.assertEqual(self.course.name,'Test Course')
        self.assertNotEqual(self.course.name, 'Course Test')
    def test_term_name(self):
        self.assertEqual(self.course.term, 'Fall 2023', 'term name does not match assigned string')
        self.assertFalse(self.course.term == '2023 Fall', 'term name does not match assigned string')

    def test_instructor(self):
        self.assertEqual(self.course.instructor, self.account, 'instructor does not match account')

