import re


def isfloat(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def validate_str_format_for_date(value: str) -> bool:
    return bool(re.match(r'^\d{2}\.\d{2}\.\d{4}$', value))
