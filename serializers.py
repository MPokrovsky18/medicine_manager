import abc

from medicine import Medicine


class BaseSerializer(abc.ABC):
    """
    Базовый класс для сериализации данных.
    """

    @abc.abstractmethod
    def serialize(self, data):
        """
        Сериализировать данные.
        """
        raise NotImplementedError(
            'Метод должен быть переопределён в классе наследнике.'
        )

    @abc.abstractmethod
    def deserialize(self, data):
        """
        Десериализировать данные.
        """
        raise NotImplementedError(
            'Метод должен быть переопределён в классе наследнике.'
        )


class JSONMedicineSerializer(BaseSerializer):
    """
    Сериализатор списка лекарств в json.
    """

    def serialize(self, medicines: list[Medicine]):
        return {'medicines': [{'name': medicine.name} for medicine in medicines]}

    def deserialize(self, data) -> list[Medicine]:
        medecines_data = data.get('medicines', [])
        medicines = []

        for medicine_data in medecines_data:
            name = medicine_data['name']
            medicine = Medicine(name)
            medicines.append(medicine)

        return medicines
