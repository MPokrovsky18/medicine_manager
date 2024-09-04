import re


MIN_LENGTH_NAME = 3


class Medicine:
    """
    Класс для представления лекарства.
    """

    def __init__(self, name) -> None:
        self.name = name

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


class MedicineManager:
    """
    Класс-менеджер для управления лекарствами.
    """
    def __init__(self) -> None:
        self.__medicines: list[Medicine] = []

    @property
    def medicine_count(self) -> int:
        """
        Длина списка лекарств.
        """
        return len(self.__medicines)

    def find_medicine(self, name: str) -> Medicine | None:
        """
        Получить объект из списка, если он существует.
        """
        target_name = Medicine.validate_name(name)

        for medicine in self.__medicines:
            if medicine.name == target_name:
                return medicine

        return None

    def add_medicine(self, name: str) -> None:
        """
        Добавить лекарство в список.
        """
        if self.find_medicine(name):
            raise ValueError('Это лекарство уже есть в списке.')

        self.__medicines.append(Medicine(name))

    def remove_medicine(self, name: str) -> None:
        """
        Удалить лекарство из списка.
        """
        target = self.find_medicine(name)

        if not target:
            raise ValueError(f'Объект с таким именем не найден: {name}')

        self.__medicines.remove(target)

    def edit_medicine(self, current_name: str, new_name: str) -> None:
        """
        Редактировать лекарство.
        """
        if self.find_medicine(new_name):
            raise ValueError(f'Объект с таким именем уже существует: {new_name}')

        medicine = self.find_medicine(current_name)

        if not medicine:
            raise ValueError(f'Объект с таким именем не найден: {current_name}')

        medicine.name = new_name

    def get_medicines_list(self) -> str:
        """
        Получить список лекарств.
        """
        if self.__medicines:
            return '\n'.join(
                f'{index+1}. {medicine.name}' for index, medicine in enumerate(self.__medicines)
            )

        return 'Список пуст!'
