from TAScheduler.models import UserAccount
from django.test import TestCase, Client, SimpleTestCase


class TestEditUser(TestCase):

    def setUp(self):
        self.monkey = Client()
        self.monkey.post("/login/", {
            "password": "Password123!",
            "email": "test@uwm.edu"
        }, follow=True)
        self.account = UserAccount.objects.register(first_name="Test", last_name="Account", email="newtest@uwm.edu",
                                                    password="Password123!", user_type="INSTRUCTOR")

    def test_valid_edit(self):
        resp = self.monkey.post("/edit_user?username=newtest@uwm.edu", {
            "firstname": "New",
            "lastname": "New",
            "email": "new@gmail.com",
            "password": "Updated123!",
            "confirmpassword": "Updated123!"
        }, follow=True)
        self.assertEqual(self.account.first_name, "New", msg="First name not updated correctly")
        self.assertEqual(self.account.last_name, "New", msg="Last name not updated correctly")
        self.assertEqual(self.account.email, "new@gmail.com", msg="Email not updated correctly")

    def test_invalidName(self):
        resp = self.monkey.post("/edit_user?username=newtest@uwm.edu", {
            "firstname": "invalid",
        }, follow=True)
        self.assertEqual(resp.context["message"], "Invalid first or last name entered", msg="Error message not sent with invalid name (no uppercase)")
        self.assertEqual(self.account.first_name, "Test", msg="Name updated with invalid name")

