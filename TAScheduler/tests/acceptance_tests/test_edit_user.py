from TAScheduler.models import UserAccount
from django.test import TestCase, Client


class TestEditUser(TestCase):

    def setUp(self):
        self.monkey = Client()
        self.monkey.post("/login/", {
            "password": "Password123!",
            "email": "test@uwm.edu"
        }, follow=True)
        self.account = UserAccount.objects.register(
            first_name="Test",
            last_name="Account",
            email="newtest@uwm.edu",
            password="Password123!",
            user_type="INSTRUCTOR")

    def test_valid_edit(self):
        self.monkey.post(f"/edit_user?username={self.account.user.username}", {
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
        resp = self.monkey.post(f"/edit_user?username={self.account.user.username}", {
            "firstname": "invalid",
        }, follow=True)
        updated_account = UserAccount.objects.get(user_id=self.account.user.id)
        self.assertEqual(updated_account.first_name, "Test", msg="First name erroneously updated with invalid name")

    def test_mismatchedPasswords(self):
        resp = self.monkey.post(f"/edit_user?username={self.account.user.username}", {
            "password": "Updated123!",
            "confirmpassword": "Password123!"
        }, follow=True)
        updated_account = UserAccount.objects.get(user_id=self.account.user.id)
        self.assertEqual(self.account.user.password, updated_account.user.password, msg="Correct error message not given when passwords dont match")

    def test_blankFields(self):
        resp = self.monkey.post(f"/edit_user?username={self.account.user.username}", {
            "firstname": "",
            "lastname": "New",
            "email": "new@gmail.com"
        }, follow=True)
        updated_account = UserAccount.objects.get(user_id=self.account.user.id)
        self.assertEqual("Test", updated_account.first_name, msg="First name changed to empty string")
        self.assertEqual("Account", updated_account.last_name, msg="Last name changed when first name empty")
        self.assertEqual("newtest@uwm.edu", updated_account.user.email, msg="Email changed when first name empty")


    def test_usedEmail(self):
        self.accounttwo = UserAccount.objects.register(
            first_name="TestTwo",
            last_name="AccountTwo",
            email="newaccount@uwm.edu",
            password="Password123!",
            user_type="ADMIN")
        resp = self.monkey.post(f"/edit_user?username={self.account.user.username}", {
            "email": "newaccount@uwm.edu"
        })
        updated_account = UserAccount.objects.get(user_id=self.account.user.id)
        self.assertEqual("newtest@uwm.edu", updated_account.user.email, msg="Email updated when user with given email already exists")

