import re

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
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True

    return has_upper and has_lower and has_digit

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

    return re.match(r"[\d()+\-]+", phone_number) is not None