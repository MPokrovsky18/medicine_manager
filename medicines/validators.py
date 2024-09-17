from datetime import date
import re


MIN_LENGTH_NAME = 3
MAX_LENGTH_NAME = 50
MAX_DELTA_YEAR = 2


class MedicineValidator:
    """
    Класс для валидации полей экземпляра типа Medicine.
    """

    @staticmethod
    def field_is_instance_else_error(
        field: object, target_type: type, field_name: str
    ) -> None:
        """
        Соответствует ли объект ожидаемому типу, иначе выбросить исключение.
        """
        if not isinstance(field, target_type):
            raise TypeError(
                f'Для поля "{field_name}" ожидался '
                + f'тип "{target_type.__name__}.". '
                + f'Получен тип "{type(field).__name__}".'
            )

    @staticmethod
    def validate_name(name: str) -> str:
        """
        Проверка валидности названия.
        """
        MedicineValidator.field_is_instance_else_error(name, str, 'name')

        validated_name = name.strip().lower()

        if not validated_name:
            raise ValueError(
                'Название не может быть пустым '
                + 'или состоять только из пробелов.'
            )

        if len(validated_name) < MIN_LENGTH_NAME:
            raise ValueError(
                f'Название должно быть не менее {MIN_LENGTH_NAME} символов.'
            )

        if len(validated_name) > MAX_LENGTH_NAME:
            raise ValueError(
                f'Название должно быть не более {MAX_LENGTH_NAME} символов.'
            )

        if validated_name.isdigit():
            raise ValueError('Название не может содержать только цифры.')

        if not re.match(r'^[a-zA-Zа-яА-яёЁ0-9 ]+$', validated_name):
            raise ValueError(
                'Название может содержать только буквы, цифры и пробелы.'
            )

        return validated_name

    @staticmethod
    def validate_id(id: int) -> int:
        """
        Проверка валидности id.
        """
        MedicineValidator.field_is_instance_else_error(id, int, 'id')

        if id <= 0:
            raise ValueError('id должен быть положительным.')

        return id

    @staticmethod
    def validate_expiration_date(expiration_date: date) -> date:
        """
        Проверка валидности даты срока годности.
        """
        MedicineValidator.field_is_instance_else_error(
            expiration_date, date, 'expiration_date'
        )

        delta_year = abs((expiration_date - date.today()).days) // 365

        if delta_year > MAX_DELTA_YEAR:
            raise ValueError(
                'Год срока годности не может отличатся '
                + f'больше чем на {MAX_DELTA_YEAR} от текущего.'
            )

        return expiration_date

    @staticmethod
    def validate_is_accepted(is_accepted: bool) -> bool:
        """
        Проверка валидности is_accepted.
        """
        MedicineValidator.field_is_instance_else_error(
            is_accepted, bool, 'is_accepted'
        )

        return is_accepted
