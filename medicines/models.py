from copy import copy
from datetime import date

from validators import MedicineValidator, MedicineStorageValidator


class Medicine:
    """
    Класс для представления лекарства.
    """

    def __init__(
            self, name: str, 
            expiration_date: date, 
            is_accepted: bool
    ) -> None:
        self.__id: int = 0
        self.name: str = name
        self.expiration_date: date = expiration_date
        self.is_accepted: bool = is_accepted

    @property
    def id(self) -> int:
        return self.__id

    def assign_id(self, value) -> None:
        """
        Присвоить id, если ранее не было установлено.
        """
        if self.__id != 0:
            raise ValueError('ID лекарства уже назначен и не может быть изменён.')

        self.__id = MedicineValidator.validate_id(value)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name: str = MedicineValidator.validate_name(value)

    @property
    def expiration_date(self) -> date:
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value: date) -> None:
        self.__expiration_date = MedicineValidator.validate_expiration_date(value)

    @property
    def is_expired(self) -> bool:
        "Возвращает True, если лекарство просрочено."
        return self.expiration_date < date.today()

    @property
    def is_accepted(self) -> str:
        return self.__is_accepted

    @is_accepted.setter
    def is_accepted(self, value: str) -> None:
        self.__is_accepted: bool = MedicineValidator.validate_is_accepted(value)

    def __str__(self) -> str:
        return self.name
    
    def __dict__(self) -> dict:
        return {
            'id': self.__id,
            'name': self.__name,
            'expiration_date': str(self.__expiration_date),
            'is_accepted': self.__is_accepted
        }


class MedicineStorage:
    """
    Представление для хранилища всех лекарств.
    """

    def __init__(self) -> None:
        self.__medicines: dict[int, Medicine] = {}
        self.__last_id: int =  0

    def check_is_not_duplicate(self, medicine: Medicine) -> bool:
        """
        Возвращает True, если нет похожих лекарств хранилище.
        """
        if not isinstance(medicine, Medicine):
            raise TypeError(f'Ожидался тип Medicine для аргумента, а получен: {type(medicine).__name__}.')

        return not any(medicine.name == current.name for current in self.__medicines)

    def __get_new_id(self) -> int:
        """
        Создает новый уникальный ID.
        """
        self.__last_id += 1
        return self.__last_id

    def add(self, medicine: Medicine) -> bool:
        """
        Добавить лекарство в хранилище.
        """
        if not isinstance(medicine, Medicine):
            raise TypeError(f'Ожидался тип Medicine для аргумента, а получен: {type(medicine).__name__}.')

        if not self.check_is_not_duplicate(medicine):
            raise ValueError(f'Похожий объект уже существует. medicine: {medicine.name}.')

        if medicine.id in self.__medicines:
            raise ValueError(f'Лекарство с ID: {medicine.id} уже существует.')

        if medicine.id == 0:
            medicine.assign_id(self.__get_new_id())
        else:
            self.__last_id = max(self.__last_id, medicine.id)

        self.__medicines[medicine.id] = copy(medicine)

    def add_multiple(self, medicines: list[Medicine]) -> None | list[dict[str, any]]:
        """
        Добавить список лекарств в хранилище.

        Лекарства, которые не были добавлены, возвращаются в списке словарей с описанием ошибки.
        """
        if not isinstance(medicines, list):
            raise TypeError(f'Метод принимает тип list[Medicine]. Получен: {type(medicines).__name__}.')

        for medicine in medicines:
            if not isinstance(medicine, Medicine):
                raise TypeError(f'Ожидался тип Medicine для всех объектов в списке, а получен: {type(medicine).__name__}.')

        not_added_with_error = []

        for medicine in medicine:
            try:
                self.add(medicine)
            except ValueError as e:
                not_added_with_error.append({
                    'medicine': medicine,
                    'error': str(e)
                })

        return not_added_with_error or None

    def remove(self, id: int) -> None:
        """
        Удалить лекарство из хранилища.
        """
        if not isinstance(id, int):
            raise TypeError('Передаваемый id должен быть типа int.')

        if id not in self.__medicines:
            raise ValueError(f'Лекарство с ID {id} не найдено.')

        del self.__medicines[id]

    def update(self, medicine: Medicine) -> None:
        """
        Обновить лекарство в хранилище.
        """
        if not isinstance(medicine, Medicine):
            raise TypeError(f'Ожидался тип Medicine для аргумента, а получен: {type(medicine).__name__}.')

        if medicine.id not in self.__medicines:
            raise ValueError(f'Лекарство с ID {medicine.id} не найдено.')

        self.__medicines[medicine.id] = copy(medicine)

    def get(self, id: int = None) -> Medicine | list[Medicine]:
        """
        Получить список всех лекарств или лекарство по ID.
        """
        if id is None:
            return sorted(
                [copy(medicine) for medicine in self.__medicines.values()],
                key=lambda x: x.id
            )

        if not isinstance(id, int):
            raise TypeError('Передаваемый id должен быть типа int.')

        if id not in self.__medicines:
            raise ValueError(f'Лекарство с ID {id} не найдено.')

        return copy(self.__medicines[id])

    def get_all_expired(self) -> list[Medicine]:
        """
        Получить список всех просроченных лекарств.
        """
        return [medicine for medicine in self.get() if medicine.is_expired]

    def get_all_accepted(self) -> list[Medicine]:
        """
        Получить список всех принимаемых лекарств.
        """
        return [medicine for medicine in self.get() if medicine.is_accepted]
