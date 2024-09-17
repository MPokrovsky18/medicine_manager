from datetime import date

from medicines.managers import Medicine


class JSONMedicineSerializer:
    """
    Сериализатор списка лекарств в json.
    """

    def serialize(self, medicines: list[Medicine]):
        """
        Сериализировать список лекарств в json.
        """
        return {
            'medicines': [medicine.to_dict() for medicine in medicines]
        }

    def deserialize(self, data) -> list[Medicine]:
        """
        Десериализировать json-данные в список лекарств.
        """
        medicines_data = data.get('medicines', [])
        medicines = []

        for medicine_data in medicines_data:
            id = medicine_data['id']
            name = medicine_data['name']
            expiration_date = date(
                *map(int, medicine_data['expiration_date'].split('-'))
            )
            is_accepted = medicine_data['is_accepted']
            medicine = Medicine(
                name=name,
                expiration_date=expiration_date,
                is_accepted=is_accepted
            )
            medicine.assign_id(id)
            medicines.append(medicine)

        return medicines
