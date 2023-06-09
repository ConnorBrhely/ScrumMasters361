import re

SPECIAL_CHARACTERS = "!@#$%^&*()_+{}|:<>?[]\;',./`~"

PASSWORD_REQUIREMENTS = "Passwords must be at least 8 characters long and contain at least one uppercase letter, " \
                        "one lowercase letter, one digit, and one special character."

def password(password_str: str):
    """
    Validates a given password to ensure it meets the minimum requirements
    :param password_str: The password to validate
    :return: True if the password is valid, False otherwise
    """
    if not password_str:
        return False

    if len(password_str) < 8:
        return False

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    # Confirm that all required characters are present
    for char in password_str:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in SPECIAL_CHARACTERS:
            has_special = True

    return has_upper and has_lower and has_digit and has_special

def email(email_str: str):
    """
    Validates a given email to ensure it is a valid email address
    :param email_str: The email to validate
    :return: True if the email is valid, False otherwise
    """
    if not email_str:
        return False

    email_str = email_str.strip()

    # Email regex from www.regexlib.com
    return re.match(r"^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$", email_str) is not None

def phone_number(phone_number_str: str):
    """
    Validates a given phone number to ensure it is a valid phone number (i.e. only 0-9, (), +, and -)
    :param phone_number_str: The phone number to validate
    :return: True if the phone number is valid, False otherwise
    """
    if not phone_number_str:
        return False
    phone_number_str = phone_number_str.strip()

    # Enforce length limits
    if len(phone_number_str) < 10 or len(phone_number_str) > 32:
        return False

    # Ensure that only valid characters are present
    for char in phone_number_str:
        if not char.isdigit() and char not in "()+-. ":
            return False

    return True

def section_number(section_number_str: str):
    """
    Validates a given section number to ensure it is a valid section number (i.e. only 0-9 and -)
    :param section_number_str: The section number to validate
    :return: True if the section number is valid, False otherwise
    """
    if not section_number_str:
        return False

    section_number_str = section_number_str.strip()
    if len(section_number_str) == 0:
        return False

    # Ensure that only valid characters are present
    for char in section_number_str:
        if not char.isdigit() and char != "-":
            return False

    return True

def course_number(course_number_str: str):
    """
    Validates a given course number to ensure it is a valid course number (i.e. only 0-9, and space)
    :param course_number_str: The course number to validate
    :return: True if the course number is valid, False otherwise
    """
    if not course_number_str:
        return False

    course_number_str = course_number_str.strip()
    if len(course_number_str) == 0:
        return False

    # Must be two words in course number
    if len(course_number_str.split()) != 2:
        return False

    course_abbrev = course_number_str.split()[0]
    course_num = course_number_str.split()[1]

    # Course abbreviation (e.g. "COMPSCI") must be between 3 and 16 characters
    if len(course_abbrev) < 3 or len(course_abbrev) > 16:
        return False
    # Course number (e.g. "101") must be 3 characters
    if len(course_num) != 3:
        return False

    # Course abbreviation must be all uppercase letters
    if not course_abbrev.isalpha() or not course_abbrev.isupper():
        return False

    # Course number must be all digits
    if not course_num.isdigit():
        return False

    return True

def name(first_name: str, last_name: str):
    """
    Validates a given first and last name to ensure they are capitalized
    :param first_name: The first name to validate
    :param last_name: The last name to validate
    :return: True if the first and last name are capitalized, False otherwise
    """
    if not first_name or not last_name:
        return False

    len_first_before = len(first_name)
    len_last_before = len(last_name)

    first_name = first_name.strip()
    last_name = last_name.strip()

    # Trailing whitespace is not allowed
    if len(first_name) != len_first_before or len(last_name) != len_last_before:
        return False

    if len(first_name) == 0 or len(last_name) == 0:
        return False

    # Names must have a capital first letter
    if first_name[0].islower() or last_name[0].islower():
        return False

    # Names must be all letters
    if not first_name.isalpha() or not last_name.isalpha():
        return False

    return True

def term(term_str: str):
    """
    Validates a given term string to ensure it is a valid term string (i.e. only 0-9 and -)
    :param term_str: The term string to validate
    :return: True if the term string is valid, False otherwise
    """
    if not term_str:
        return False

    # Must be two words in term string
    term_str = term_str.strip()
    term_split = term_str.split()
    if len(term_split) != 2:
        return False

    term_season = term_split[0]
    term_year = term_split[1]

    # Only allow valid seasons
    if term_season not in ["Spring", "Summer", "Fall"]:
        return False

    # Year must be 4 digits
    if len(term_year) != 4 or not term_year.isdigit():
        return False

    return True

def year(year_str: str):
    """
    Validates a given year string to ensure it is a valid year string (i.e. only 0-9)
    :param year_str: The year string to validate
    :return: True if the year string is valid, False otherwise
    """
    if not year_str:
        return False

    # Year must be 4 digits, sorry to any schools in the year 10,000
    year_str = year_str.strip()
    if len(year_str) != 4 or not year_str.isdigit():
        return False

    return True

def home_address(address_str: str):
    if not address_str:
        return False

    # Address must be at least 3 words
    address_split = address_str.strip().split()
    if len(address_split) < 3:
        return False

    address_number = address_split[0]
    address_name = "".join(address_split[1:])

    # Address number must be numeric
    if not address_number.isnumeric():
        return False

    # Address name must be capitalized
    if not address_name[0].isupper():
        return False

    # All words in address must be all letters or periods
    for char in address_name:
        if not char.isalpha() and not char == ".":
            return False

    return True

def office_hours(office_hours_str: str):
    if not office_hours_str:
        return False

    office_hours_str = office_hours_str.strip()
    if len(office_hours_str) == 0:
        return False

    return True