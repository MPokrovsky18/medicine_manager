import re


class Medicine:
    """
    Класс для представления лекарства.
    """
    def __init__(self, name) -> None:
        self.name = self.validate_name(name)

    def __str__(self) -> str:
        return self.name

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

        if not re.match(r'^[a-zA-Zа-яА-яёЁ0-9 ]+$', validated_name):
            raise ValueError('Название может содержать только буквы, цифры и пробелы.')

        return validated_name


class MedicineManager:
    """
    Класс-менеджер для управления лекарствами.
    """
    def __init__(self) -> None:
        self.medicines: list[Medicine] = []

    def add_medicine(self, medicine: Medicine) -> bool:
        """
        Добавить лекарство в список.
        """
        if medicine:
            self.medicines.append(medicine)
            return True

        return False

    def remove_medicine(self, medicine_id: int) -> bool:
        """
        Удалить лекарство из списка.
        """
        if medicine_id >= 0 and medicine_id < len(self.medicines):
            self.medicines.pop(medicine_id)
            return True

        return False

    def edit_medicine(self, medicine_id: int, name: str) -> bool:
        """
        Редактировать лекарство.
        """
        if name and medicine_id >= 0 and medicine_id < len(self.medicines):
            self.medicines[medicine_id].name = name
            return True
        
        return False

    def get_medicines_list(self) -> str:
        """
        Получить список лекарств.
        """
        if self.medicines:
            return '\n'.join(
                f'{index}. {medicine.name}' for index, medicine in enumerate(self.medicines)
            )
        
        return 'Список пуст!'