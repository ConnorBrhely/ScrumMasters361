from TAScheduler.models import UserAccount
from django.test import TestCase, Client


class TestCreateUser(TestCase):

    def setUp(self):
        self.monkey = Client()
        self.type = "Admin"
        self.name = "test"
        self.password = "Password123"
        self.confirm_password = "Password123"
        self.email = "test@gmail.com"

    def test_create_user(self):
        resp = self.monkey.post("/create_user/", {
            "type": self.type,
            "name": self.name,
            "password": self.password,
            "confirmpassword": self.confirm_password,
            "email": self.email
        }, follow=True)
        self.assertEqual(UserAccount.objects.count(), 1, msg="User not successfully created with valid information")
        self.assertEqual(resp.context["message"],
                         "User successfully created",
                         msg="User not successfully created with valid information")

    def test_invalid_password(self):
        self.password = "password123"
        self.confirm_password = "password123"
        resp = self.monkey.post("/create_user/", {
            "type": self.type,
            "name": self.name,
            "password": self.password,
            "confirmpassword": self.confirm_password,
            "email": self.email
        }, follow=False)
        self.assertEqual(resp.context["message"],
                         "Passwords does not contain 8 characters with 1 uppercase letter and 1 number",
                         msg="Correct error message not displayed with invalid password")

    def test_short_password(self):
        self.password = "Test1"
        self.confirm_password = "Test1"
        resp = self.monkey.post("/create_user/", {"type": self.type, "name": self.name, "password": self.password, "confirmpassword": self.confirm_password, "email": self.email}, follow=False)
        self.assertEqual(UserAccount.objects.count(), 0, msg="object created with invalid password")
        self.assertEqual(resp.context["message"], "Passwords does not contain 8 characters with 1 uppercase letter and 1 number", msg="Correct error message not displayed with invalid password")

    def test_non_matching_passwords(self):
        self.confirm_password = "Password1234"
        resp = self.monkey.post("/create_user/", {"type": self.type, "name": self.name, "password": self.password, "confirmpassword": self.confirm_password, "email": self.email}, follow=False)
        self.assertEqual(UserAccount.objects.count(), 0, msg="object created with non matching passwords")
        self.assertEqual(resp.context["message"], "Passwords do not match", msg="Correct error message not displayed with non matching passwords")

    def test_invalid_email(self):
        self.email = "test@gmail"
        resp = self.monkey.post("/create_user/", {"type": self.type, "name": self.name, "password": self.password, "confirmpassword": self.confirm_password, "email": self.email}, follow=False)
        self.assertEqual(UserAccount.objects.count(), 0, msg="object created with invalid email")
        self.assertEqual(resp.context["message"], "Invalid email entered", msg="Correct error message not displayed with invalid email")

    def test_blank_fields(self):
        self.password = ""
        self.name = ""
        resp = self.monkey.post("/create_user/", {"type": self.type, "name": self.name, "password": self.password, "confirmpassword": self.confirm_password, "email": self.email}, follow=False)
        self.assertEqual(UserAccount.objects.count(), 0, msg="object created with blank fields")
        self.assertEqual(resp.context["message"], "One or more blank field detected", msg="Correct error message not displayed with blank fields")

    def test_duplicate_email(self):
        resp = self.monkey.post("/create_user/", {"type": self.type, "name": self.name, "password": self.password, "confirmpassword": self.confirm_password, "email": self.email}, follow=False)
        resp = self.monkey.post("/create_user/", {"type": self.type, "name": self.name, "password": self.password, "confirmpassword": self.confirm_password, "email": self.email}, follow=False)
        self.assertEqual(resp.context["message"], "User with email already exists", msg="Correct error message not displayed when duplicate email entered")

