import unittest

from medicine import Medicine, MedicineManager


class TestMedicineApp(unittest.TestCase):
    def test_add_medicine(self):
        manager = MedicineManager()
        medicine = Medicine('placebo')

        manager.add_medicine(medicine)

        self.assertEqual(len(manager.medicines), 1)
        self.assertEqual(manager.medicines[0].name, medicine.name)

    def test_remove_medicine(self):
        manager = MedicineManager()
        manager.medicines = [Medicine('placebo')]

        manager.remove_medicine(0)

        self.assertEqual(len(manager.medicines), 0)

    def test_edit_medicine(self):
        manager = MedicineManager()
        manager.medicines = [Medicine('placebo')]
        new_name = 'not placebo'
        manager.edit_medicine(0, new_name)

        self.assertEqual(len(manager.medicines), 1)
        self.assertEqual(manager.medicines[0].name, new_name)

    def test_get_medicines_list(self):
        manager = MedicineManager()
        manager.medicines = [Medicine('placebo'), Medicine('not placebo')]
        medicines_str = f'0. {manager.medicines[0].name}\n1. {manager.medicines[1].name}'

        self.assertEqual(manager.get_medicines_list(), medicines_str)


if __name__ == '__main__':
    unittest.main()
