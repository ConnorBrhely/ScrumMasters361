from TAScheduler.models import UserAccount, Course, Section
from django.test import TestCase

class TestModelSection(TestCase):
    def setUp(self):
            self.user = UserAccount.objects.create(
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

        # TODO: Add tests for Section model

    def test_updateName(self):
        self.section.update_name(self, 'new name')
        self.save()
        self.assertEqual('new name', self.section.name, msg="section has new name")

    def test_noName(self):
        self.section.update_name(self, '')
        self.save()
        self.assertEqual('', self.section.name, msg="section has no name")



    def test_update_name(self):
        new_name = 'New Section Name'
        self.section.update_name(new_name)
        self.assertEqual(self.section.name, new_name)

    def test_add_ta(self):
        self.section.add_ta(self.user)
        self.assertEqual(self.section.tas.first(), self.user)
    def test_add_non_ta_user_as_ta(self):
        with self.assertRaises(ValueError):
            self.section.add_ta(User.objects.create(
                name='Test Student',
                type='STUDENT',
            ))

    def test_remove_ta(self):
        self.section.tas.add(self.user)
        self.section.remove_ta(self.user)
        self.assertFalse(self.section.tas.exists())

        #TODO: Add tests for Section model

    def test_add_to_section(self):
        self.user.add_to_section('Test Section')
        self.assertTrue(self.section.tas.exists())

