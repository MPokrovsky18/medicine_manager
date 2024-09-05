import unittest

from medicine import Medicine, MedicineManager


class TestMedicineManager(unittest.TestCase):
    """
    Тестируем MedicineManager.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.medicine_name_1 = 'medicine 1'
        cls.medicine_name_2 = 'medicine 2'
        cls.medicine_name_3 = 'medicine 3'
        cls.medicine_name_empty = ''
        cls.medicine_name_not_str = 1
        cls.medicine_name_short = 'ab'

    def setUp(self) -> None:
        self.manager = MedicineManager()
        self.manager_1count = MedicineManager()
        self.manager_2count = MedicineManager()

        self.manager_1count._MedicineManager__medicines.append(
            Medicine(self.medicine_name_1)
        )
        self.manager_2count._MedicineManager__medicines.extend(
            [Medicine(self.medicine_name_1), Medicine(self.medicine_name_2)]
        )

    def test_empty_medicine_manager_count(self) -> None:
        self.assertEqual(self.manager.medicine_count, 0)

    def test_medicine_manager_count(self):
        test_data = (
            (self.manager_1count, 1),
            (self.manager_2count, 2)
        )

        for manager, expected_result in test_data:
            with self.subTest(
                f'Метод вернул не верный результат.',
                expected_result=expected_result
            ):
                self.assertEqual(manager.medicine_count, expected_result)

    def test_find_medicine_in_empty_manager(self):
        self.assertEqual(
            self.manager.find_medicine(self.medicine_name_1),
            None,
            msg='При попытке получить объект из пустого списка, получен не None.'
        )

    def test_find_medicine_is_instance(self):
        test_data = (
            self.medicine_name_1,
            self.medicine_name_2,
        )

        for name in test_data:
            medicine = self.manager_2count.find_medicine(name)

            with self.subTest(
                f'Ожидался тип {Medicine.__name__}, получен {type(medicine).__name__}',
                name = name,
            ):
                self.assertIsInstance(medicine, Medicine)

    def test_find_medicine(self):
        test_data = (
            self.medicine_name_1,
            self.medicine_name_2,
        )

        for name in test_data:
            medicine = self.manager_2count.find_medicine(name)

            with self.subTest(
                msg=f'Ожидалось лекарство с именем {name}, но получено {medicine.name}',
            ):
                self.assertEqual(medicine.name, name)
    
    def test_find_medicine_not_in_manager(self):
        self.assertEqual(
            self.manager_2count.find_medicine(self.medicine_name_3),
            None,
            msg='При попытке получить не существующий объект, получен не None.'
        )
    
    def test_find_medicine_with_uncorrect_data(self):
        test_data = (
            (self.medicine_name_empty, ValueError, 'Пустое имя должно вызвать ValueError'),
            (self.medicine_name_short, ValueError, 'Слишком короткое имя должно вызвать ValueError'),
            (self.medicine_name_not_str, TypeError, 'Неверный тип данных должен вызвать TypeError')
        )

        for name, error, msg in test_data:
            with self.subTest(msg=msg):
                with self.assertRaises(error):
                    self.manager_2count.find_medicine(name)

    def test_add_medicine(self):
        test_name = 'placebo'

        self.manager.add_medicine(test_name)

        self.assertEqual(self.manager.medicine_count, 1)
        self.assertEqual(self.manager.find_medicine(test_name).name, test_name)

    def test_remove_medicine(self):
        test_name = 'placebo'
        self.manager.add_medicine(test_name)

        self.manager.remove_medicine(test_name)

        self.assertEqual(self.manager.medicine_count, 0)

    def test_edit_medicine(self):
        test_name = 'placebo'
        new_name = 'not placebo'
        self.manager.add_medicine(test_name)
        self.manager.edit_medicine(test_name, new_name)

        self.assertEqual(self.manager.medicine_count, 1)
        self.assertEqual(self.manager.find_medicine(new_name).name, new_name)

    def test_get_medicines_list(self):
        test_name_1 = 'placebo'
        test_name_2 = 'not placebo'
        self.manager.add_medicine(test_name_1)
        self.manager.add_medicine(test_name_2)
        medicines_str = f'1. {test_name_1}\n2. {test_name_2}'

        self.assertEqual(self.manager.get_medicines_list(), medicines_str)


if __name__ == '__main__':
    unittest.main()
