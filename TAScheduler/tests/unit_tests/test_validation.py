from TAScheduler.models import UserAccount, Course, Section
from django.test import TestCase
from ...common import validate

class TestValidation(TestCase):
    def test_validate_password(self):
        self.assertTrue(validate.password("TestPassword123!"), msg="Valid password failed validation")
        self.assertFalse(validate.password(""), msg="Blank password passed validation")
        self.assertFalse(validate.password("testpassword123!"), msg="Password with no uppercase passed validation")
        self.assertFalse(validate.password("TESTPASSWORD123!"), msg="Password with no lowercase passed validation")
        self.assertFalse(validate.password("TestPassword!"), msg="Password with no number passed validation")
        self.assertFalse(validate.password("TestPassword123"), msg="Password with no special character passed validation")
        self.assertFalse(validate.password("Tpass1!"), msg="Password with too few characters passed validation")

    def test_validate_email(self):
        self.assertTrue(validate.email("email@gmail.com"), msg="Valid email failed validation")
        self.assertFalse(validate.email(""), msg="Blank email passed validation")
        self.assertFalse(validate.email("emailgmail.com"), msg="Email with no @ passed validation")
        self.assertFalse(validate.email("email@gmailcom"), msg="Email with no . passed validation")
        self.assertFalse(validate.email("emailgmailcom"), msg="Email with no @ or . passed validation")

    def test_validate_phone_number(self):
        self.assertTrue(validate.phone_number("+1 (414) 555-1234"), msg="Valid phone number failed validation")
        self.assertFalse(validate.phone_number(""), msg="Blank phone number passed validation")
        self.assertFalse(validate.phone_number("+1 (414) 555-1234!"), msg="Phone number with illegal char passed validation")

    def test_validate_address(self):
        self.assertTrue(validate.address("1234 Fake Street"), "Valid address failed validation")
        self.assertTrue(validate.address("1234 Fake St."), "Valid address with abbreviation failed validation")
        self.assertFalse(validate.address(""), "Blank address passed validation")
        self.assertFalse(validate.address("OneTwoThreeFour Fake St."), "Address with no starting digits passed validation")
        self.assertFalse(validate.address("Fake St."), "Address with no numbers passed validation")
        self.assertFalse(validate.address("12-34 Fake St."), "Address with invalid characters in number passed validation")
        self.assertFalse(validate.address("1234 Fake St-"), "Address with invalid characters in name passed validation")
