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

    def test_getTitle(self):
        self.assertEqual(self.course.getTitle(), 'Test Course')
    def test_setTitle(self):
        with self.assertRaises(ValueError, msg='Course name cannot be empty'):
            self.course.setTitle("")
        with self.assertRaises(ValueError, msg='Course name must contain characters other than whitespace'):
            self.course.setTitle(' \t\n')
        with self.assertNotEqual(self.course.getTitle(), 'New Name'):
            self.course.setTitle('New Name')

    def test_get_after_set(self):
        with self.assertRaises(ValueError, msg='Course name not updated properly after set'):
            self.course.setTitle('New Name')
            self.assertEqual(self.coruse.getTitle(), 'New Name', msg='expectred title to be \"New Name\"')


