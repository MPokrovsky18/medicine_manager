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
            'medicines': [medicine.__dict__ for medicine in medicines]
        }

    def deserialize(self, data) -> list[Medicine]:
        """
        Десериализировать json-данные в список лекарств.
        """
        medecines_data = data.get('medicines', [])
        medicines = []

        for medicine_data in medecines_data:
            id = medecines_data['id']
            name = medicine_data['name']
            expiration_date = medicine_data['expiration_date']
            is_accepted = medicine_data['is_accepted']
            medicine = Medicine(
                name=name,
                expiration_date=expiration_date,
                is_accepted=is_accepted
            )
            medicine.assign_id(id)
            medicines.append(medicine)

        return medicines
