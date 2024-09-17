from medicines.models import Medicine, MedicineStorage
from medicines.validators import MedicineValidator


class MedicineManager:
    """
    Класс-менеджер для управления лекарствами.
    """

    def __init__(self, medicines: list[Medicine] = None) -> None:
        self.__medicine_storage: MedicineStorage = MedicineStorage()

        if medicines:
            self.__medicine_storage.add_multiple(medicines)

    @property
    def medicines(self):
        """
        Получить копию списка лекарств.
        """
        return self.__medicine_storage.get()

    @property
    def medicine_count(self) -> int:
        """
        Длина списка лекарств.
        """
        return self.__medicine_storage.count

    def find_medicine(self, name: str) -> Medicine | None:
        """
        Получить объект из списка, если он существует.
        """
        target_name = MedicineValidator.validate_name(name)

        for medicine in self.__medicine_storage.get():
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
        self.__medicine_storage.add(Medicine(name))

    def remove_medicine(self, name: str) -> None:
        """
        Удалить лекарство из списка.
        """
        target = self.check_exist_medicine_or_rise(name)
        self.__medicine_storage.remove(target.id)

    def edit_medicine(self, current_name: str, new_name: str) -> None:
        """
        Редактировать лекарство.
        """
        medicine = self.check_exist_medicine_or_rise(current_name)
        self.check_exist_medicine_or_rise(new_name, exists=False)
        medicine.name = new_name
        self.__medicine_storage.update(medicine)

    def get_medicines_list(self) -> str:
        """
        Получить список лекарств.
        """
        medicines = self.__medicine_storage.get()

        if medicines:
            return '\n'.join(
                f'{index+1}. {medicine.name}'
                for index, medicine in enumerate(medicines)
            )

        return 'Список пуст!'
