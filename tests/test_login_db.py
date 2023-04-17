from django.test import TestCase
from TAScheduler.models import User, Course, Section

class TestLogin(TestCase):
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

    def test_delete_login(self):
        self.user.delete()
        self.assertEqual(User.objects.count(), 0, 'User was not deleted')
        self.assertEqual(Course.objects.get(pk=self.course.pk).instructor, None,
                         'Course instructor was not set to None after user deletion')

    def test_delete_course(self):
        self.course.delete()
        self.assertEqual(Course.objects.count(), 0, 'Course was not deleted')
        self.assertEqual(Section.objects.count(), 0, 'Section was not cascade deleted after course deletion')