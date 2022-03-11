
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, RegexValidator, EmailValidator, MaxValueValidator, MinValueValidator, DecimalValidator


def validate_user(value):
    if value is None:
        raise ValidationError("Please Enter A Name")
    return value