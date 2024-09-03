import unittest

from main import (
    add_medicine,
    remove_medicine,
    edit_medicine,
    get_medicines_list,
    Medicine
)


class TestMedicineApp(unittest.TestCase):
    def test_add_medicine(self):
        medicines = []
        medicine = Medicine('placebo')
        add_medicine(medicine, medicine_list=medicines)

        self.assertEqual(len(medicines), 1)
        self.assertEqual(medicines[0].name, medicine.name)


    def test_remove_medicine(self):
        medicines = [Medicine('placebo')]
        remove_medicine(0, medicine_list=medicines)
        self.assertEqual(len(medicines), 0)

    def test_edit_medicine(self):
        medicines = [Medicine('placebo')]
        new_name = 'not placebo'
        edit_medicine(0, new_name, medicine_list=medicines)

        self.assertEqual(len(medicines), 1)
        self.assertEqual(medicines[0].name, new_name)

    def test_get_medicines_list(self):
        medicines = [Medicine('placebo'), Medicine('not placebo')]
        medicines_str = f'0. {medicines[0].name}\n1. {medicines[1].name}'

        self.assertEqual(get_medicines_list(medicine_list=medicines), medicines_str)


if __name__ == '__main__':
    unittest.main()
