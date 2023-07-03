import re


def strong_password(password):
    errors = list()
    regex_lower_case = re.compile(r"(?=.*[a-z])")
    regex_upper_case = re.compile(r"(?=.*?[A-Z])")
    regex_one_number = re.compile(r"(?=.*?[0-9])")
    regex_special_character = re.compile(r"(?=.*[@$!%*?&-(),.~#;:])")

    if not password:
        errors.append("Password must not be empty")

    if len(password) < 8:
        errors.append("Password must have at least 8 characters")

    if not regex_upper_case.match(password):
        errors.append("Password must have at least one uppercase letter")

    if not regex_lower_case.match(password):
        errors.append("Password must have at least one lowercase letter")

    if not regex_one_number.match(password):
        errors.append("Password must have at least one number")

    if not regex_special_character.match(password):
        errors.append("Password must have at least one special character.")

    return errors
