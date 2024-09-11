from datetime import date

from validators import MedicineValidator


class Medicine:
    """
    Класс для представления лекарства.
    """

    def __init__(self, id, name, expiration_date, is_accepted) -> None:
        self.__id: int = MedicineValidator.validate_id(id)
        self.name: str = name
        self.expiration_date: date = expiration_date
        self.is_accepted: bool = is_accepted

    def __str__(self) -> str:
        return self.name

    @property
    def id(self) -> int:
        return self.__id

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
