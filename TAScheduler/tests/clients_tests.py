from django.test import TestCase
from TAScheduler.models import User, Course, Section


class TestUserModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            name='Test User',
            email='testuser@example.com',
            password='testpassword',
            type=User.UserType.STUDENT,
            home_address='123 Main St.',
            phone_number='555-555-5555',
            office_hours='MWF 1-3',
        )

        self.instructor = User.objects.create(
            name='Test Instructor',
            email='testinstructor@example.com',
            password='testpassword',
            type=User.UserType.PROFESSOR,
            home_address='123 Main St.',
            phone_number='555-555-5555',
            office_hours='MWF 1-3',
        )

        self.course = Course.objects.create(
            name='Test Course',
            term='Fall 2023',
            instructor=self.instructor,
        )

        self.section = Section.objects.create(
            name='Test Section',
            location='Test Location',
            time='Test Time',
            course=self.course,
        )

    def test_user_creation(self):
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.password, 'testpassword')
        self.assertEqual(self.user.type, User.UserType.STUDENT)
        self.assertEqual(self.user.home_address, '123 Main St.')
        self.assertEqual(self.user.phone_number, '555-555-5555')
        self.assertEqual(self.user.office_hours, 'MWF 1-3')

    def test_instructor_creation(self):
        self.assertEqual(self.instructor.name, 'Test Instructor')
        self.assertEqual(self.instructor.email, 'testinstructor@example.com')
        self.assertEqual(self.instructor.password, 'testpassword')
        self.assertEqual(self.instructor.type, User.UserType.PROFESSOR)
        self.assertEqual(self.instructor.home_address, '123 Main St.')
        self.assertEqual(self.instructor.phone_number, '555-555-5555')
        self.assertEqual(self.instructor.office_hours, 'MWF 1-3')

    def test_course_instructor(self):
        self.assertEqual(self.course.instructor, self.instructor)

    def test_course_student_enrollment(self):
        self.user.courses.add(self.course)
        self.assertEqual(self.user.courses.count(), 1)

    def test_course_section_creation(self):
        self.assertEqual(self.section.course, self.course)

    def test_user_deletion(self):
        self.user.delete()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Course.objects.get(pk=self.course.pk).instructor, None)

    def test_course_deletion(self):
        self.course.delete()
        self.assertEqual(Course.objects.count(), 0)
        self.assertEqual(Section.objects.count(), 0)

    def test_section_deletion(self):
        self.section.delete()
        self.assertEqual(Section.objects.count(), 0)
        self.assertEqual(Course.objects.get(pk=self.course.pk).sections.count(), 0)

    def test_user_update(self):
        self.user.name = 'New Test Name'
        self.user.email = 'newemail@example.com'
        self.user.password = 'newpassword'
        self.user.type = User.UserType.ADMIN
        self.user.home_address = '456 Elm St.'
        self.user.phone_number = '555-555-5556'
        self.user.office_hours = 'TR 2-4'
        self.user.save()

        updated_user = User.objects.get(pk=self.user.pk)

