import re


MIN_LENGTH_NAME = 3
MAX_LENGTH_NAME = 50


class MedicineValidator:
    """
    Класс для валидации полей экземпляра типа Medicine.
    """

    @staticmethod
    def validate_name(name: str) -> str:
        """
        Проверка валидности названия.
        """
        if not isinstance(name, str):
            raise TypeError(
                f'Передана не строка. arg: {name} - type: {type(name).__name__}.'
            )

        validated_name = name.strip().lower()

        if not validated_name:
            raise ValueError('Название не может быть пустым или состоять только из пробелов.')

        if len(validated_name) < MIN_LENGTH_NAME:
            raise ValueError(f'Название должно быть не менее {MIN_LENGTH_NAME} символов.')

        if len(validated_name) < MAX_LENGTH_NAME:
            raise ValueError(f'Название должно быть не более {MAX_LENGTH_NAME} символов.')

        if not re.match(r'^[a-zA-Zа-яА-яёЁ0-9 ]+$', validated_name):
            raise ValueError('Название может содержать только буквы, цифры и пробелы.')

        return validated_name
    
    @staticmethod
    def validate_id(id: int):
        """
        Проверка валидности id.
        """
        return id

    @staticmethod
    def validate_expiration_date(expiration_date):
        """
        Проверка валидности даты срока годности.
        """
        return expiration_date

    @staticmethod
    def validate_is_accepted(is_accepted: bool):
        """
        Проверка валидности is_accepted.
        """
        return is_accepted