import re


MIN_LENGTH_NAME = 3


class Medicine:
    """
    Класс для представления лекарства.
    """

    def __init__(self, id, name, expiration_date, is_accepted) -> None:
        self.id = id
        self.name = name
        self.expiration_date = expiration_date
        self.is_accepted = is_accepted

    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = self.validate_name(value)

    @staticmethod
    def validate_name(name: str) -> str:
        """
        Проверка валидности названия лекарства.
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

        if not re.match(r'^[a-zA-Zа-яА-яёЁ0-9 ]+$', validated_name):
            raise ValueError('Название может содержать только буквы, цифры и пробелы.')

        return validated_name
