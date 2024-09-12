from datetime import date

from validators import MedicineValidator, MedicineStorageValidator


class Medicine:
    """
    Класс для представления лекарства.
    """

    def __init__(self, id, name, expiration_date, is_accepted) -> None:
        self.id: int = id
        self.name: str = name
        self.expiration_date: date = expiration_date
        self.is_accepted: bool = is_accepted

    def __str__(self) -> str:
        return self.name

    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, value) -> int:
        self.__id = MedicineValidator.validate_id(id)

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
    def is_accepted(self) -> str:
        return self.__is_accepted

    @is_accepted.setter
    def is_accepted(self, value: str) -> None:
        self.__is_accepted: bool = MedicineValidator.validate_is_accepted(value)


class MedicineStorage:
    """
    Представление для хранилища всех лекарств.
    """

    def __init__(self) -> None:
        self.__medicines: dict[int, Medicine] = {}
        self.__last_id: int =  0

    def check_duplicate(self, medicine: Medicine) -> bool:
        duplicate = [current for current in self.__medicines.values() if current.name == medicine.name]

        return False if duplicate else True

    def __get_new_id(self) -> int:
        self.__last_id += 1
        return self.__last_id

    def add(self, medicine: Medicine) -> bool:
        if self.check_duplicate(medicine):
            medicine.id = self.__get_new_id()
            self.__medicines[medicine.id] = medicine
            return True

        return False
 
    def clear_and_add_multiple(self, medicines: list[Medicine]) -> None:
        self.__medicines = MedicineStorageValidator.validate_medicines(medicines)
        self.__last_id = max(self.__medicines.keys())

    def remove(self, id) -> bool:
        if id in self.__medicines:
            del self.__medicines[id]
            return True
        
        return False

    def update(self, medicine: Medicine) -> bool:
        if medicine.id in self.__medicines:
            self.__medicines[medicine.id] = medicine
            return True
        
        return False

    def get(self, id) -> Medicine | None:
        return self.__medicines.get(id)

# TODO: Выбрасывать исключения в методах вместо возвращения True/False
# Добавить методы для фильтрации и возвращения объектов списком
# Доработать метод проверки дупликатов
# Добавить докстринги
