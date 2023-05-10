import re

SPECIAL_CHARACTERS = "!@#$%^&*()_+{}|:<>?[]\;',./`~"

PASSWORD_REQUIREMENTS = "Passwords must be at least 8 characters long and contain at least one uppercase letter, " \
                        "one lowercase letter, one digit, and one special character."

def validate_password(password: str):
    """
    Validates a given password to ensure it meets the minimum requirements
    :param password: The password to validate
    :return: True if the password is valid, False otherwise
    """
    if not password:
        return False

    if len(password) < 8:
        return False

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in SPECIAL_CHARACTERS:
            has_special = True

    return has_upper and has_lower and has_digit and has_special

def validate_email(email):
    """
    Validates a given email to ensure it is a valid email address
    :param email: The email to validate
    :return: True if the email is valid, False otherwise
    """
    if not email:
        return False

    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def validate_phone_number(phone_number: str):
    """
    Validates a given phone number to ensure it is a valid phone number (i.e. only 0-9, (), +, and -)
    :param phone_number: The phone number to validate
    :return: True if the phone number is valid, False otherwise
    """
    if not phone_number:
        return False
    if len(phone_number) < 10:
        return False
    for char in phone_number:
        if not char.isdigit() and char not in "()+- ":
            return False

    return True

def validate_section_number(section_number: str):
    """
    Validates a given section number to ensure it is a valid section number (i.e. only 0-9 and -)
    :param section_number: The section number to validate
    :return: True if the section number is valid, False otherwise
    """
    if not section_number:
        return False

    for char in section_number:
        if not char.isdigit() and char != "-":
            return False

    return True

def validate_name(first_name: str, last_name: str):
    """
    Validates a given first and last name to ensure they are capitalized
    :param first_name: The first name to validate
    :param last_name: The last name to validate
    :return: True if the first and last name are capitalized, False otherwise
    """
    if not first_name or not last_name:
        return False

    if first_name[0].islower() or last_name[0].islower():
        return False

    if not first_name.isalpha() or not last_name.isalpha():
        return False

    return True

def validate_term(term_string: str):
    """
    Validates a given term string to ensure it is a valid term string (i.e. only 0-9 and -)
    :param term_string: The term string to validate
    :return: True if the term string is valid, False otherwise
    """
    if not term_string:
        return False

    term_split = term_string.split()
    if len(term_split) != 2:
        return False

    term_season = term_split[0]
    term_year = term_split[1]

    if term_season not in ["Spring", "Summer", "Fall"]:
        return False

    if len(term_year) != 4 or not term_year.isdigit():
        return False

    return True