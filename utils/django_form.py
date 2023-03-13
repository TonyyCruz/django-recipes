import re

from django.forms import ValidationError


def strong_password(password):
    regex = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    )
    if not regex.match(password):
        raise ValidationError((
            "Password must have at least one uppercase letter, "
            "one lowercase letter one number and one special character. "
            "The length should be at least 8 characters."
        ),
            code="Invalid"
        )
