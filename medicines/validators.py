from datetime import date
import re


MIN_LENGTH_NAME = 3
MAX_LENGTH_NAME = 50
MAX_DELTA_YEAR = 2


class MedicineValidator:
    """
    Класс для валидации полей экземпляра типа BaseMedicine.
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
    def validate_id(id: int) -> int:
        """
        Проверка валидности id.
        """
        MedicineValidator.field_is_instance_else_error(id, int, 'id')

        if id <= 0:
            raise ValueError('id должен быть положительным.')

        return id

    @staticmethod
    def validate_title(title: str) -> str:
        """
        Проверка валидности названия.
        """
        MedicineValidator.field_is_instance_else_error(title, str, 'title')

        validated_title = title.strip().lower()

        if not validated_title:
            raise ValueError(
                'Название не может быть пустым '
                + 'или состоять только из пробелов.'
            )

        if len(validated_title) < MIN_LENGTH_NAME:
            raise ValueError(
                f'Название должно быть не менее {MIN_LENGTH_NAME} символов.'
            )

        if len(validated_title) > MAX_LENGTH_NAME:
            raise ValueError(
                f'Название должно быть не более {MAX_LENGTH_NAME} символов.'
            )

        if validated_title.isdigit():
            raise ValueError('Название не может содержать только цифры.')

        if not re.match(r'^[a-zA-Zа-яА-яёЁ0-9 ]+$', validated_title):
            raise ValueError(
                'Название может содержать только буквы, цифры и пробелы.'
            )

        return validated_title

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
    def validate_capacity(capacity: float) -> float:
        """
        Проверка валидности capacity.
        """
        MedicineValidator.field_is_instance_else_error(
            capacity, float, 'capacity'
        )

        if capacity <= 0:
            raise ValueError('capacity должен быть положительным.')

        return capacity

    @staticmethod
    def validate_current_quantity(quantity: float) -> float:
        """
        Проверка валидности quantity.
        """
        MedicineValidator.field_is_instance_else_error(
            quantity, float, 'quantity'
        )

        if quantity < 0:
            raise ValueError('quantity не может быть отрицательным.')

        return quantity
