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
        self.monkey.post(f"/edit_user/?username={self.account.user.username}", {
            "firstname": "New",
            "lastname": "New",
            "email": "new@gmail.com",
            "password": "Updated123!",
            "confirmpassword": "Updated123!"
        }, follow=True)
        updated_account = UserAccount.objects.get(user_id=self.account.user.id)
        self.assertEqual(updated_account.first_name, "New", msg="First name not updated correctly")
        self.assertEqual(updated_account.last_name, "New", msg="Last name not updated correctly")
        self.assertEqual(updated_account.user.email, "new@gmail.com", msg="Email not updated correctly")

    def test_invalidName(self):
        resp = self.monkey.post("/edit_user?username=newtest@uwm.edu", {
            "firstname": "invalid",
        }, follow=True)
        updated_account = UserAccount.objects.get(user_id=self.account.user.id)
        self.assertEqual(updated_account.first_name, "Test", msg="First name erroneously updated with invalid name")

