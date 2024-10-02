from copy import copy

from medicines.base import BaseMedicine


DEFAULT_DROP_VOLUME = 0.05


class Pills(BaseMedicine):
    """
    Класс представления лекарства в виде таблеток.
    """

    def __str__(self) -> str:
        return super().__str__() + 'таб.'

    def take_unit(self, units_quantity: float = 1) -> None:
        if self.can_take_unit and self.quantity >= units_quantity:
            self.quantity -= units_quantity


class Drops(BaseMedicine):
    """
    Класс представления лекарства в виде капель.
    """

    def __str__(self) -> str:
        return super().__str__() + 'мл.'

    def take_unit(self, units_quantity: float) -> None:
        if self.can_take_unit:
            taking_volume = units_quantity * DEFAULT_DROP_VOLUME

            if self.quantity >= taking_volume:
                self.quantity -= taking_volume


class MedicineStorage:
    """
    Представление для хранилища всех лекарств.
    """

    def __init__(self) -> None:
        self.__medicines: dict[int, BaseMedicine] = {}
        self.__last_id: int = 0

    @property
    def count(self):
        """
        Количество лекарств в хранилище.
        """
        return len(self.__medicines)

    def check_is_not_duplicate(self, medicine: BaseMedicine) -> bool:
        """
        Возвращает True, если нет похожих лекарств хранилище.
        """
        if not isinstance(medicine, BaseMedicine):
            raise TypeError(
                'Ожидался тип Medicine для аргумента, '
                + f'а получен: {type(medicine).__name__}.'
            )

        return not any(
            medicine.name == current.name
            for current in self.__medicines.values()
        )

    def __get_new_id(self) -> int:
        """
        Создает новый уникальный ID.
        """
        self.__last_id += 1
        return self.__last_id

    def add(self, medicine: BaseMedicine) -> bool:
        """
        Добавить лекарство в хранилище.
        """
        if not isinstance(medicine, BaseMedicine):
            raise TypeError(
                'Ожидался тип Medicine для аргумента, '
                + f'а получен: {type(medicine).__name__}.'
            )

        if not self.check_is_not_duplicate(medicine):
            raise ValueError(
                'Похожий объект уже существует. '
                + f'medicine: {medicine.name}.'
            )

        if medicine.id in self.__medicines:
            raise ValueError(f'Лекарство с ID: {medicine.id} уже существует.')

        if medicine.id == 0:
            medicine.assign_id(self.__get_new_id())
        else:
            self.__last_id = max(self.__last_id, medicine.id)

        self.__medicines[medicine.id] = copy(medicine)

    def add_multiple(
        self, medicines: list[BaseMedicine]
    ) -> None | list[dict[str, any]]:
        """
        Добавить список лекарств в хранилище.

        Лекарства, которые не были добавлены,
        возвращаются в списке словарей с описанием ошибки.
        """
        if not isinstance(medicines, list):
            raise TypeError(
                'Метод принимает тип list[Medicine]. '
                + f'Получен: {type(medicines).__name__}.'
            )

        for medicine in medicines:
            if not isinstance(medicine, BaseMedicine):
                raise TypeError(
                    'Ожидался тип Medicine для всех объектов в списке, '
                    + f'а получен: {type(medicine).__name__}.'
                )

        not_added_with_error = []

        for medicine in medicines:
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

    def update(self, medicine: BaseMedicine) -> None:
        """
        Обновить лекарство в хранилище.
        """
        if not isinstance(medicine, BaseMedicine):
            raise TypeError(
                'Ожидался тип Medicine для аргумента, '
                + f'а получен: {type(medicine).__name__}.'
            )

        if medicine.id not in self.__medicines:
            raise ValueError(f'Лекарство с ID {medicine.id} не найдено.')

        if not self.check_is_not_duplicate(medicine):
            raise ValueError(
                'Похожий объект уже существует. '
                + f'medicine: {medicine.name}.'
            )

        self.__medicines[medicine.id] = copy(medicine)

    def get(self, id: int = None) -> BaseMedicine | list[BaseMedicine]:
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

    def get_all_expired(self) -> list[BaseMedicine]:
        """
        Получить список всех просроченных лекарств.
        """
        return [medicine for medicine in self.get() if medicine.is_expired]
