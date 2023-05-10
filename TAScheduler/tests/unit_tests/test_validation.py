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
        self.assertFalse(validate.phone_number("+1 414 555 1234"), msg="Phone number without parenthesis failed validation")
        self.assertFalse(validate.phone_number("+1-414-555-1234"), msg="Phone number with dash instead of space failed validation")

    def test_validate_address(self):
        self.assertTrue(validate.address("1234 Ammar Street"), "Valid address failed validation")
        self.assertTrue(validate.address("1234 Ammar St."), "Valid address with abbreviation failed validation")
        self.assertFalse(validate.address(""), "Blank address passed validation")
        self.assertFalse(validate.address("OneTwoThreeFour Ammar St."), "Address with no starting digits passed validation")
        self.assertFalse(validate.address("Ammar St."), "Address with no numbers passed validation")
        self.assertFalse(validate.address("12-34 Ammar St."), "Address with invalid characters in number passed validation")
        self.assertFalse(validate.address("1234 Ammar St-"), "Address with invalid characters in name passed validation")

    def test_phone_number(self):
        self.assertTrue(validate.phone_number("+1 (414) 555-1234"), msg="Valid phone number failed validation")
        self.assertFalse(validate.phone_number(""), msg="Blank phone number passed validation")
        self.assertFalse(validate.phone_number("+1 (414) 555-1234!"), msg="Phone number with illegal char passed validation")
        self.assertFalse(validate.phone_number("+14145551234"), msg="Phone number without spaces or parenthesis failed validation")
        self.assertFalse(validate.phone_number("+1 414 555 1234"), msg="Phone number without parenthesis failed validation")
        self.assertFalse(validate.phone_number("+1-414-555-1234"), msg="Phone number with dash instead of space failed validation")

    def test_section_number(self):
        self.assertTrue(validate.section_number("001"), msg="Valid section number failed validation")
        self.assertTrue(validate.section_number("001-001"), msg="Valid section number with dash failed validation")
        self.assertFalse(validate.section_number(""), msg="Blank section number passed validation")
        self.assertFalse(validate.section_number("001!"), msg="Section number with illegal character passed validation")
        self.assertFalse(validate.section_number("001.001"), msg="Section number with dot instead of dash failed validation")
        self.assertFalse(validate.section_number("001-"), msg="Section number with no ending digits failed validation")
        self.assertFalse(validate.section_number("-001"), msg="Section number with no starting digits failed validation")

    def test_validate_office_hours(self):
        self.assertTrue(validate.office_hours("MWF 9-10"), msg="Valid office hours failed validation")
        self.assertTrue(validate.office_hours("MWF 8:30-10:00"), msg="Valid office hours with colons failed validation")
        self.assertTrue(validate.office_hours("T 3-4"), msg="Valid office hours with single day failed validation")
        self.assertTrue(validate.office_hours("MW 10-11, F 1-2"), msg="Valid office hours with multiple days failed validation")
        self.assertFalse(validate.office_hours(""), msg="Blank office hours passed validation")
        self.assertFalse(validate.office_hours(" "), msg="Blank office hours with whitespace passed validation")

    def test_validate_office_hours(self):
        self.assertTrue(validate.office_hours("M 3:00-5:00, W 2:00-4:00"), msg="Valid office hours failed validation")
        self.assertFalse(validate.office_hours(""), msg="Blank office hours passed validation")
        self.assertFalse(validate.office_hours("Mon 3:00-5:00, Wed 2:00-4:00"), msg="Invalid day format passed validation")
        self.assertFalse(validate.office_hours("M 3:00-5:00, W 14:00-16:00"), msg="Invalid time format passed validation")
        self.assertFalse(validate.office_hours("M 3:00-5:00, W"), msg="Invalid format passed validation")
