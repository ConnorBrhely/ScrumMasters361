from TAScheduler.models import UserAccount, Course, Section
from django.test import TestCase
from ...common import validate

class TestValidation(TestCase):
    def test_validate_password(self):
        self.assertTrue(validate.validate_password("TestPassword123!"), msg="Valid password failed validation")
        self.assertFalse(validate.validate_password("testpassword123!"), msg="Password with no uppercase succeeded validation")
        self.assertFalse(validate.validate_password("TESTPASSWORD123!"), msg="Password with no lowercase succeeded validation")
        self.assertFalse(validate.validate_password("TestPassword!"), msg="Password with no number succeeded validation")
        self.assertFalse(validate.validate_password("TestPassword123"), msg="Password with no special character succeeded validation")
        self.assertFalse(validate.validate_password("Tpass1!"), msg="Password with too few characters succeeded validation")

    def test_validate_email(self):
        self.assertTrue(validate.validate_email("email@gmail.com"), msg="Valid email failed validation")
        self.assertFalse(validate.validate_email("emailgmail.com"), msg="Email with no @ succeeded validation")
        self.assertFalse(validate.validate_email("email@gmailcom"), msg="Email with no . succeeded validation")
        self.assertFalse(validate.validate_email("emailgmailcom"), msg="Email with no @ or . succeeded validation")

    def test_validate_phone_number(self):
        self.assertTrue(validate.validate_phone_number("+1 (414) 555-1234"), msg="Valid phone number failed validation")
        self.assertFalse(validate.validate_phone_number("+1 (414) 555-1234!"), msg="Phone number with illegal char succeeded validation")