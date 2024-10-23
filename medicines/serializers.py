from datetime import datetime

from medicines.managers import BaseMedicine, MEDICINES_ENUM


class JSONMedicineSerializer:
    """
    Сериализатор списка лекарств в json.
    """
    def get_medicine_as_dict_with_type(self, medicine: BaseMedicine) -> dict:
        """
        Вернуть лекарство в виде словаря с указанием типа лекарства.
        """
        medicine_dict = medicine.to_dict()

        if isinstance(medicine, MEDICINES_ENUM[0][1]):
            medicine_dict['medicine_type'] = 0
        else:
            medicine_dict['medicine_type'] = 1

        return medicine_dict

    def serialize(self, medicines: list[BaseMedicine]):
        """
        Сериализировать список лекарств в json.
        """
        return {
            'medicines': [
                self.get_medicine_as_dict_with_type(medicine)
                for medicine in medicines
            ]
        }

    def deserialize(self, data) -> list[BaseMedicine]:
        """
        Десериализировать json-данные в список лекарств.
        """
        medicines_data = data.get('medicines', [])
        medicines = []

        for medicine_data in medicines_data:
            id = medicine_data['id']
            title = medicine_data['title']
            capacity = float(medicine_data['capacity'])
            current_quantity = float(medicine_data['current_quantity'])
            medicine_type = medicine_data['medicine_type']

            expiration_date = datetime.strptime(
                medicine_data['expiration_date'], '%Y-%m-%d'
            ).date()

            medicine = MEDICINES_ENUM[medicine_type][1](
                title=title,
                expiration_date=expiration_date,
                capacity=capacity,
                current_quantity=current_quantity
            )
            medicine.assign_id(id)
            medicines.append(medicine)

        return medicines
