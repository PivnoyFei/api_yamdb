import datetime as dt

from django.core.exceptions import ValidationError


def year_validator(value):
    year = dt.datetime.now().year
    if year < value:
        raise ValidationError('Неправильный год издания произведения!')
    return value
