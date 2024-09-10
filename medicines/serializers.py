from medicines.managers import Medicine


class JSONMedicineSerializer:
    """
    Сериализатор списка лекарств в json.
    """

    def serialize(self, medicines: list[Medicine]):
        """
        Сериализировать список лекарств в json.
        """
        return {'medicines': [{'name': medicine.name} for medicine in medicines]}

    def deserialize(self, data) -> list[Medicine]:
        """
        Десериализировать json-данные в список лекарств.
        """
        medecines_data = data.get('medicines', [])
        medicines = []

        for medicine_data in medecines_data:
            name = medicine_data['name']
            medicine = Medicine(name)
            medicines.append(medicine)

        return medicines
