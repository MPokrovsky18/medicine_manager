from abc import ABC, abstractmethod
from datetime import date

from medicines.validators import MedicineValidator as mv


class BaseMedicine(ABC):
    """
    Абстрактный класс лекарства.
    """

    def __init__(
        self,
        title: str,
        expiration_date: date,
        capacity: float,
        quantity: float
    ) -> None:
        self.__id: int = 0
        self.title: str = title
        self.expiration_date: date = expiration_date
        self.capacity: float = capacity
        self.quantity: float = quantity

    @property
    def id(self) -> int:
        return self.__id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        self.__title: str = mv.validate_title(value)

    @property
    def expiration_date(self) -> date:
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, value) -> None:
        self.__expiration_date = mv.validate_expiration_date(value)

    @property
    def capacity(self) -> float:
        return self.__capacity

    @capacity.setter
    def capacity(self, value) -> None:
        self.__capacity = mv.validate_capacity(value)

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value) -> None:
        self.__quantity = mv.validate_quantity(value)

    def __str__(self) -> str:
        return (
            f'{self.title}: годен до {self.expiration_date};'
            + f'{self.quantity}/{self.capacity}.'
        )

    def assign_id(self, value) -> None:
        """
        Присвоить id, если ранее не был установлен.
        """
        if self.__id != 0:
            raise ValueError(
                'ID лекарства уже назначен и не может быть изменён.'
            )

        self.__id = mv.validate_id(value)

    def update(
        self,
        title: str = None,
        expiration_date: date = None,
        capacity: float = None,
        quantity: float = None
    ) -> None:
        """
        Обновить значения объекта.
        """
        if title:
            self.title = title

        if expiration_date:
            self.expiration_date = expiration_date

        if capacity:
            self.capacity = capacity

        if quantity:
            self.quantity = quantity

    def to_dict(self) -> dict:
        """
        Вернуть объект как словарь.
        """
        return {
            'id': self.__id,
            'title': self.__name,
            'expiration_date': str(self.__expiration_date),
            'capacity': self.__capacity,
            'quantity': self.__quantity,
        }

    @abstractmethod
    def take(self):
        """
        Принять лекарство.
        """
        pass
