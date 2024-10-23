from copy import copy

from medicines.base import BaseMedicine


DEFAULT_DROP_VOLUME = 0.05


class Pills(BaseMedicine):
    """
    Класс представления лекарства в виде таблеток.
    """

    def __str__(self) -> str:
        return 'Таблетки - ' + super().__str__() + ' таб.'

    def take_unit(self, units_quantity: float = 1) -> None:
        if self.can_take_unit and self.current_quantity >= units_quantity:
            self.current_quantity -= units_quantity


class Drops(BaseMedicine):
    """
    Класс представления лекарства в виде капель.
    """

    def __str__(self) -> str:
        return 'Капли - ' + super().__str__() + ' мл.'

    def take_unit(self, units_quantity: float) -> None:
        if self.can_take_unit:
            taking_volume = units_quantity * DEFAULT_DROP_VOLUME

            if self.current_quantity >= taking_volume:
                self.current_quantity -= taking_volume


class MedicineStorage:
    """
    Представление для хранилища всех лекарств.
    """

    def __init__(self) -> None:
        self.__medicines: dict[int, BaseMedicine] = {}
        self.__last_id: int = 0

    @property
    def count(self) -> int:
        """
        Количество лекарств в хранилище.
        """
        return len(self.__medicines)

    def __get_new_id(self) -> int:
        """
        Создает новый уникальный ID.
        """
        self.__last_id += 1
        return self.__last_id

    def add(self, medicine: BaseMedicine) -> None:
        """
        Добавить лекарство в хранилище.
        """
        if not isinstance(medicine, BaseMedicine):
            raise TypeError(
                'Ожидался тип BaseMedicine для аргумента, '
                + f'а получен: {type(medicine).__name__}.'
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
                'Метод принимает тип list[BaseMedicine]. '
                + f'Получен: {type(medicines).__name__}.'
            )

        for medicine in medicines:
            if not isinstance(medicine, BaseMedicine):
                raise TypeError(
                    'Ожидался тип BaseMedicine для всех объектов в списке, '
                    + f'а получен: {type(medicine).__name__}.'
                )

        not_added_with_error = []

        for medicine in medicines:
            try:
                self.add(copy(medicine))
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

        self.__medicines[medicine.id] = copy(medicine)

    def check_compliance(self, medicine: BaseMedicine, **kwargs):
        """
        Проверить соответсвие лекарства по параметрам.
        """
        medicine_data = medicine.to_dict()

        for param_name, value in kwargs.items():
            if param_name == 'target_type':
                if (
                    value is not None
                    and not isinstance(medicine, value)
                ):
                    return False
                else:
                    continue

            target_param = medicine_data.get(param_name)

            if (
                target_param is not None
                and value is not None
                and target_param != value
            ):
                return False

        return True

    def get(
        self, **kwargs
    ) -> BaseMedicine | list[BaseMedicine] | None:
        """
        Получить список всех лекарств или лекарство по ID.
        """
        if not kwargs:
            return sorted(
                [copy(medicine) for medicine in self.__medicines.values()],
                key=lambda x: x.id
            )

        if kwargs.get('id'):
            target_id = kwargs.pop('id')

            if not isinstance(target_id, int):
                raise TypeError('Передаваемый id должен быть типа int.')

            if target_id not in self.__medicines:
                raise ValueError(f'Лекарство с ID {target_id} не найдено.')

            target_medicine = self.__medicines[target_id]

            if self.check_compliance(target_medicine, **kwargs):
                return copy(target_medicine)
            else:
                return None

        filtered_medicines = []

        for medicine in self.__medicines.values():
            if self.check_compliance(medicine, **kwargs):
                filtered_medicines.append(copy(medicine))

        return sorted(filtered_medicines, key=lambda x: x.id)

    def get_all_expired(self) -> list[BaseMedicine]:
        """
        Получить список всех просроченных лекарств.
        """
        return [medicine for medicine in self.get() if medicine.is_expired]
