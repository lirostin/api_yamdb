import datetime

from django.core.exceptions import ValidationError


def validator_year(value):
    """Проверяем, что год не больше текущего."""

    todays_year = datetime.date.today().year
    if value > todays_year:
        raise ValidationError(
            f'ОШИБКА: год выпуска {value} больше '
            f'чем текущий {todays_year}'
        )
    return value
