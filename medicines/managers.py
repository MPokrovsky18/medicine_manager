from medicines.models import Medicine


class MedicineManager:
    """
    Класс-менеджер для управления лекарствами.
    """

    def __init__(self, medicines: list[Medicine] = None) -> None:
        self.__medicines: list[Medicine] = self.validate_medicines(medicines)

    def validate_medicines(self, medicines: list[Medicine]) -> list[Medicine]:
        """
        Проверка элементов передаваемого списка на соответствие типу Medicine.
        """
        if not medicines:
            return []

        if isinstance(medicines, Medicine):
            return [medicines]

        if not isinstance(medicines, list):
            raise TypeError(
                f'Передан другой тип. Ожидается list[{Medicine.__name__}]'
            )

        if not all(isinstance(x, Medicine) for x in medicines):
            raise TypeError(
                f'Не все объекты в списке типа {Medicine.__name__}.'
            )

        return medicines

    @property
    def medicines(self):
        """
        Получить копию списка лекарств.
        """
        return self.__medicines.copy()

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

    def check_exist_medicine_or_rise(
        self, name: str, exists: bool = True
    ) -> Medicine | None:
        """
        Проверить объект на существование или отсутствие в списке.
        """
        medicine = self.find_medicine(name)

        if not medicine and exists:
            raise ValueError(f'Объект с таким именем не найден: {name}')

        if medicine and not exists:
            raise ValueError(f'Объект с таким именем уже существует: {name}')

        return medicine if exists else None

    def add_medicine(self, name: str) -> None:
        """
        Добавить лекарство в список.
        """
        self.check_exist_medicine_or_rise(name, exists=False)
        self.__medicines.append(Medicine(name))

    def remove_medicine(self, name: str) -> None:
        """
        Удалить лекарство из списка.
        """
        target = self.check_exist_medicine_or_rise(name)
        self.__medicines.remove(target)

    def edit_medicine(self, current_name: str, new_name: str) -> None:
        """
        Редактировать лекарство.
        """
        medicine = self.check_exist_medicine_or_rise(current_name)
        self.check_exist_medicine_or_rise(new_name, exists=False)
        medicine.name = new_name

    def get_medicines_list(self) -> str:
        """
        Получить список лекарств.
        """
        if self.__medicines:
            return '\n'.join(
                f'{index+1}. {medicine.name}'
                for index, medicine in enumerate(self.__medicines)
            )

        return 'Список пуст!'
