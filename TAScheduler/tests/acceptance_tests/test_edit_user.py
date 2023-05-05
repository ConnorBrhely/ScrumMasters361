from TAScheduler.models import UserAccount
from django.test import TestCase, Client, SimpleTestCase

class TestEditUser(TestCase):

    def setUp(self):
        self.monkey = Client()
        self.monkey.post("/login/", {
            "password": "Password123!",
            "email": "test@uwm.edu"
        }, follow=True)
        self.account = UserAccount.objects.register(first_name="test", last_name="account", email="newtest@uwm.edu", password="Password123!", user_type="INSTRUCTOR")


    def test_valid_edit(self):
        resp = self.monkey.post("/edit_user?username=newtest@uwm.edu", {
            "firstname": "new",
            "lastname": "new",
            "email": "new@gmail.com",
            "password": "Updated123!",
            "confirmpassword": "Updated123!"
        }, follow=True)
        print(resp.context)
        """self.assertRedirects(response=resp, expected_url="/accounts/", status_code=301, msg_prefix="User not successfully edited with valid information")"""
        self.assertEqual(self.account.first_name, "new", msg="First name not updated correctly")
        self.assertEqual(self.account.last_name, "new", msg="Last name not updated correctly")
        self.assertEqual(self.account.email, "new@gmail.com", msg="Email not updated correctly")