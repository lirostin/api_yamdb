import re

from django.core.exceptions import ValidationError


def validate_username(value):
    """Проверка на недопустимые username."""
    if value.lower() == 'me':
        raise ValidationError('"me" - Недопустимое имя пользователя.')

    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
        raise ValidationError(
            (f'Недопустимый набор символов: "{value}"'),
            params={'value': value},
        )
