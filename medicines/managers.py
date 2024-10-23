from datetime import date

from medicines.base import BaseMedicine
from medicines.factories import MedicineFactory
from medicines.models import MedicineStorage, Pills, Drops
from medicines.validators import MedicineValidator


MEDICINES_ENUM = (
    ('капли', Drops),
    ('таблетки', Pills)
)


class MedicineManager:
    """
    Класс-менеджер для управления лекарствами.
    """

    def __init__(self, medicines: list[BaseMedicine] = None) -> None:
        self.__medicine_storage: MedicineStorage = MedicineStorage()

        if medicines:
            self.__medicine_storage.add_multiple(medicines)

    @property
    def medicine_count(self) -> int:
        """
        Длина списка лекарств.
        """
        return self.__medicine_storage.count

    def get_medicines_by_filters(
        self,
        id: int | None = None,
        type_index: int | None = None,
        title: str | None = None,
        expiration_date: date | None = None,
        capacity: float | None = None,
        current_quantity: float | None = None
    ) -> list[BaseMedicine]:
        """
        Получить список лекарств по фильтру.
        """
        passed_params = {}

        if id:
            passed_params['id'] = id

        if type_index:
            if type_index == 0:
                target_type = Drops
            elif type_index == 1:
                target_type = Pills

            passed_params['target_type'] = target_type

        if title:
            passed_params['title'] = MedicineValidator.validate_title(title)

        if expiration_date:
            passed_params['expiration_date'] = expiration_date

        if capacity:
            passed_params['capacity'] = capacity

        if current_quantity:
            passed_params['current_quantity'] = current_quantity

        return self.__medicine_storage.get(**passed_params)

    def add_medicine(
        self,
        medicine_type: int,
        title: str,
        expiration_date: date,
        capacity: float,
        current_quantity: float
    ) -> None:
        """
        Добавить лекарство в список.
        """
        if medicine_type == 0:
            new_medicine = MedicineFactory.get_new_drops(
                title=title,
                expiration_date=expiration_date,
                capacity=capacity,
                current_quantity=current_quantity
            )
        elif medicine_type == 1:
            new_medicine = MedicineFactory.get_new_pills(
                title=title,
                expiration_date=expiration_date,
                capacity=capacity,
                current_quantity=current_quantity
            )

        self.__medicine_storage.add(new_medicine)

    def remove_medicine(self, id: int) -> None:
        """
        Удалить лекарство из списка.
        """
        self.__medicine_storage.remove(id)

    def edit_medicine(
        self,
        id: int,
        medicine_type: int | None = None,
        title: str | None = None,
        expiration_date: date | None = None,
        capacity: float | None = None,
        current_quantity: float | None = None
    ) -> None:
        """
        Редактировать лекарство.
        """
        medicine = self.get_medicines_by_filters(id=id)

        if medicine_type and not isinstance(
            medicine, MEDICINES_ENUM[medicine_type][1]
        ):
            if medicine_type == 0:
                new_medicine = MedicineFactory.get_new_drops(
                    title=medicine.title,
                    expiration_date=medicine.expiration_date,
                    capacity=medicine.capacity,
                    current_quantity=medicine.current_quantity
                )
            elif medicine_type == 1:
                new_medicine = MedicineFactory.get_new_pills(
                    title=medicine.title,
                    expiration_date=medicine.expiration_date,
                    capacity=medicine.capacity,
                    current_quantity=medicine.current_quantity
                )

                new_medicine.assign_id(medicine.id)
                medicine = new_medicine

        medicine.update(
            title=title,
            expiration_date=expiration_date,
            capacity=capacity,
            current_quantity=current_quantity
        )

        self.__medicine_storage.update(medicine)
