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
    print(password)

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

def validate_phone_number(phone_number):
    """
    Validates a given phone number to ensure it is a valid phone number (i.e. only 0-9, (), +, and -)
    :param phone_number: The phone number to validate
    :return: True if the phone number is valid, False otherwise
    """
    if not phone_number:
        return False

    for char in phone_number:
        if not char.isdigit() and char not in "()+- ":
            return False

    return True
