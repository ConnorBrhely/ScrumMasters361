from TAScheduler.models import UserAccount, Course, Section
from django.test import TestCase
from ...common import validate

class TestValidation(TestCase):
    def test_validate_password(self):
        self.assertTrue(validate.password("TestPassword123!"), msg="Valid password failed validation")
        self.assertTrue(validate.password("TESTPASSWORd123!"), msg="Valid password failed validation")

    def test_validate_password_invalid(self):
        self.assertFalse(validate.password("testpassword123!"), msg="Password with no uppercase passed validation")
        self.assertFalse(validate.password("TESTPASSWORD123!"), msg="Password with no lowercase passed validation")
        self.assertFalse(validate.password("TestPassword!"), msg="Password with no number passed validation")
        self.assertFalse(validate.password("TestPassword123"), msg="Password with no special character passed validation")
        self.assertFalse(validate.password("Tpass1!"), msg="Password with too few characters passed validation")

    def test_validate_password_blank(self):
        self.assertFalse(validate.password(None), msg="None password passed validation")
        self.assertFalse(validate.password(""), msg="Blank password passed validation")

    def test_validate_email(self):
        self.assertTrue(validate.email("email@gmail.com"), msg="Valid email failed validation")
        self.assertTrue(validate.email("email123@gmail.com"), msg="Valid email with numbers failed validation")

    def test_validate_email_invalid(self):
        self.assertFalse(validate.email("emailgmail.com"), msg="Email with no @ passed validation")
        self.assertFalse(validate.email("email@gmailcom"), msg="Email with no . passed validation")
        self.assertFalse(validate.email("emailgmailcom"), msg="Email with no @ or . passed validation")
        self.assertFalse(validate.email("email@"), msg="Email with no domain passed validation")
        self.assertFalse(validate.email("@gmail.com"), msg="Email with no username passed validation")

    def test_validate_email_blank(self):
        self.assertFalse(validate.email(None), msg="None email passed validation")
        self.assertFalse(validate.email(""), msg="Blank email passed validation")
        self.assertFalse(validate.email(" \t\n"), msg="Blank email passed validation")

    def test_validate_email_blank(self):
        self.assertFalse(validate.email(None), msg="None email passed validation")
        self.assertFalse(validate.email(""), msg="Blank email passed validation")
        self.assertFalse(validate.email(" \t\n"), msg="Blank email passed validation")

    def test_validate_phone_number_invalid(self):
        self.assertFalse(validate.phone_number("+1 (414) 555-1234!"), msg="Phone number with illegal char passed validation")
        self.assertFalse(validate.phone_number("1?414555?1234"), msg="Phone number with illegal char passed validation")

    def test_validate_phone_number_invalid_length(self):
        self.assertFalse(validate.phone_number("12345"), msg="Phone number with too few digits passed validation")
        self.assertFalse(validate.phone_number("123456789012345678901234567890123"), msg="Phone number with too many digits passed validation")

    def test_validate_phone_number_blank(self):
        self.assertFalse(validate.phone_number(None), msg="None phone number passed validation")
        self.assertFalse(validate.phone_number(""), msg="Blank phone number passed validation")
        self.assertFalse(validate.phone_number(" \t\n"), msg="Blank phone number passed validation")

    def test_validate_address(self):
        self.assertTrue(validate.home_address("1234 Ammar Street"), "Valid address failed validation")
        self.assertTrue(validate.home_address("1234 Ammar St."), "Valid address with abbreviation failed validation")

    def test_validate_address_invalid_num(self):
        self.assertFalse(validate.home_address("OneTwoThreeFour Ammar St."), "Address with no starting digits passed validation")
        self.assertFalse(validate.home_address("Ammar St."), "Address with no numbers passed validation")
        self.assertFalse(validate.home_address("12-34 Ammar St."), "Address with invalid characters in number passed validation")

    def test_validate_address_invalid_name(self):
        self.assertFalse(validate.home_address("1234 Ammar St-"), "Address with invalid characters in name passed validation")
        self.assertFalse(validate.home_address("1234 Am__mar --St."), "Address with invalid characters in name passed validation")

    def test_validate_address_blank(self):
        self.assertFalse(validate.home_address(None), "None address passed validation")
        self.assertFalse(validate.home_address(""), "Blank address passed validation")
        self.assertFalse(validate.home_address(" \t\n"), "Blank address with whitespace passed validation")

    def test_validate_blank_address(self):
        self.assertFalse(validate.home_address(None), "None address passed validation")
        self.assertFalse(validate.home_address(""), "Blank address passed validation")
        self.assertFalse(validate.home_address(" \t\n"), "Blank address with whitespace passed validation")

    def test_phone_number(self):
        self.assertTrue(validate.phone_number("+1 (414) 555-1234"), msg="Valid phone number failed validation")
        self.assertFalse(validate.phone_number("+1 (414) 555-1234!"), msg="Phone number with illegal char passed validation")

    def test_validate_blank_phone_number(self):
        self.assertFalse(validate.phone_number(None), msg="None phone number passed validation")
        self.assertFalse(validate.phone_number(""), msg="Blank phone number passed validation")
        self.assertFalse(validate.phone_number(" \t\n"), msg="Blank phone number with whitespace passed validation")

    def test_validate_office_hours(self):
        self.assertTrue(validate.office_hours("MWF 9-10"), msg="Valid office hours failed validation")
        self.assertTrue(validate.office_hours("MWF 8:30-10:00"), msg="Valid office hours with colons failed validation")
        self.assertTrue(validate.office_hours("T 3-4"), msg="Valid office hours with single day failed validation")
        self.assertTrue(validate.office_hours("MW 10-11, F 1-2"), msg="Valid office hours with multiple days failed validation")

    def test_validate_blank_office_hours(self):
        self.assertFalse(validate.office_hours(None), msg="None office hours passed validation")
        self.assertFalse(validate.office_hours(""), msg="Blank office hours passed validation")
        self.assertFalse(validate.office_hours(" \t\n"), msg="Blank office hours with whitespace passed validation")

    def test_validate_section_numbers(self):
        self.assertTrue(validate.section_number("003"), msg="Valid section number failed validation")
        self.assertTrue(validate.section_number("003-555"), msg="Valid section number with hyphens failed validation")
        self.assertFalse(validate.section_number("ZeroZeroThree"), msg="Section number with alpha characters passed validation")
        self.assertFalse(validate.section_number("0 0\t3"), msg="Section number with whitespace passed validation")

    def test_validate_blank_section_number(self):
        self.assertFalse(validate.section_number(None), msg="None section number passed validation")
        self.assertFalse(validate.section_number(""), msg="Blank section number passed validation")
        self.assertFalse(validate.section_number("  \t\n"), msg="Blank section number with whitespace passed validation")

    def test_validate_name(self):
        self.assertTrue(validate.name("John", "Doe"), msg="Valid name failed validation")
        self.assertFalse(validate.name("john", "doe"), msg="Lowercase name passed validation")
        self.assertFalse(validate.name("j0hn", "d0e"), msg="Name with digits passed validation")

    def test_validate_blank_name(self):
        self.assertFalse(validate.name("  ", "\t"), msg="Name with whitespace passed validation")
        self.assertFalse(validate.name("", ""), msg="Blank name passed validation")

    def test_validate_blank_course_number(self):
        self.assertFalse(validate.course_number(None), msg="None course number passed validation")
        self.assertFalse(validate.course_number(""), msg="Blank course number passed validation")
        self.assertFalse(validate.course_number("  \t"), msg="Blank course number with whitespace passed validation")

    def test_validate_valid_course_number(self):
        self.assertTrue(validate.course_number("COMPSCI 361"), msg="Valid course number failed validation")
        self.assertTrue(validate.course_number("ENG 310"), msg="Valid course number failed validation")

    def test_validate_course_number_length_mismatch(self):
        self.assertFalse(validate.course_number("COMPSCI 3611"), msg="Course number with too many digits passed validation")
        self.assertFalse(validate.course_number("COMPSCI 36"), msg="Course number with too few digits passed validation")
        self.assertFalse(validate.course_number("COMPUTERSCIENCECOURSE 361"), msg="Course number with too many letters passed validation")
        self.assertFalse(validate.course_number("COMPSCI361"), msg="Course number with no space passed validation")
        self.assertFalse(validate.course_number("COMP SCI 361"), msg="Course number with too many spaces passed validation")

    def test_validate_course_number_invalid_abbrev(self):
        self.assertFalse(validate.course_number("C0MPSC1 361"), msg="Valid course number failed validation")
        self.assertFalse(validate.course_number("3NG 310"), msg="Valid course number failed validation")
        self.assertFalse(validate.course_number("C 361"), msg="Course number with too few letters passed validation")
        self.assertFalse(validate.course_number("ZeroZeroThree"), msg="Course number with alpha characters passed validation")
        self.assertFalse(validate.course_number("001"), msg="Course number with no abbreviation passed validation")
        self.assertFalse(validate.course_number("0 0\t3"), msg="Course number with whitespace passed validation")

    def test_validate_year_valid(self):
        self.assertTrue(validate.year("2020"), msg="Valid year failed validation")
        self.assertTrue(validate.year("1969"), msg="Pre-Unix-epoch year failed validation")

    def test_validate_year_invalid(self):
        self.assertFalse(validate.year("TwentyTwenty"), msg="Year with alpha characters passed validation")
        self.assertFalse(validate.year("2 0\t2 0"), msg="Year with whitespace passed validation")

    def test_validate_year_blank(self):
        self.assertFalse(validate.year(""), msg="Blank year passed validation")
        self.assertFalse(validate.year("  \t"), msg="Blank year with whitespace passed validation")