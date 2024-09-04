import unittest

from medicine import MedicineManager


class TestMedicineApp(unittest.TestCase):
    def test_medicine_count(self):
        manager = MedicineManager()
        test_name_1 = 'placebo'
        test_name_2 = 'not placebo'

        self.assertEqual(manager.medicine_count, 0)

        manager.add_medicine(test_name_1)
        self.assertEqual(manager.medicine_count, 1)

        manager.add_medicine(test_name_2)
        self.assertEqual(manager.medicine_count, 2)
    
    def test_get_medicine(self):
        manager = MedicineManager()
        test_name_1 = 'placebo'
        test_name_2 = 'not placebo'
        test_name_3 = 'not medicine'
        manager.add_medicine(test_name_1)
        manager.add_medicine(test_name_2)

        medicine_1 = manager.find_medicine(test_name_1)
        medicine_2 = manager.find_medicine(test_name_2)
        medicine_3 = manager.find_medicine(test_name_3)

        self.assertEqual(manager.medicine_count, 2)
        self.assertEqual(medicine_1.name, test_name_1)
        self.assertEqual(medicine_2.name, test_name_2)
        self.assertEqual(medicine_3, None)


    def test_add_medicine(self):
        manager = MedicineManager()
        test_name = 'placebo'

        manager.add_medicine(test_name)

        self.assertEqual(manager.medicine_count, 1)
        self.assertEqual(manager.find_medicine(test_name).name, test_name)

    def test_remove_medicine(self):
        manager = MedicineManager()
        test_name = 'placebo'
        manager.add_medicine(test_name)

        manager.remove_medicine(test_name)

        self.assertEqual(manager.medicine_count, 0)

    def test_edit_medicine(self):
        manager = MedicineManager()
        test_name = 'placebo'
        new_name = 'not placebo'
        manager.add_medicine(test_name)
        manager.edit_medicine(test_name, new_name)

        self.assertEqual(manager.medicine_count, 1)
        self.assertEqual(manager.find_medicine(new_name).name, new_name)

    def test_get_medicines_list(self):
        manager = MedicineManager()
        test_name_1 = 'placebo'
        test_name_2 = 'not placebo'
        manager.add_medicine(test_name_1)
        manager.add_medicine(test_name_2)
        medicines_str = f'1. {test_name_1}\n2. {test_name_2}'

        self.assertEqual(manager.get_medicines_list(), medicines_str)


if __name__ == '__main__':
    unittest.main()
