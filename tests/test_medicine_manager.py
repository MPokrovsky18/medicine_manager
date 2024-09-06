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
        cls.medicine_not_allowed_symbols = '.[]@medicine'

        cls.test_uncorrect_data = (
            (
                cls.medicine_name_empty, ValueError,
                'Пустое имя должно вызвать ValueError'
            ),
            (
                cls.medicine_name_short, ValueError,
                'Слишком короткое имя должно вызвать ValueError'
            ),
            (
                cls.medicine_name_not_str, TypeError,
                'Неверный тип данных должен вызвать TypeError'
            ),
            (
                cls.medicine_not_allowed_symbols, ValueError,
                'Имя с неразрешенными символами должно вызвать ValueError'
            )
        )

    def setUp(self) -> None:
        self.empty_manager = MedicineManager()
        self.manager_1count = MedicineManager()
        self.manager_2count = MedicineManager()

        self.manager_1count._MedicineManager__medicines.append(
            Medicine(self.medicine_name_1)
        )
        self.manager_2count._MedicineManager__medicines.extend(
            [Medicine(self.medicine_name_1), Medicine(self.medicine_name_2)]
        )

    def test_empty_medicine_manager_count(self) -> None:
        self.assertEqual(self.empty_manager.medicine_count, 0)

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
            self.empty_manager.find_medicine(self.medicine_name_1),
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
        for name, error, msg in self.test_uncorrect_data:
            with self.subTest(msg=msg):
                with self.assertRaises(
                    error,
                    msg=f'Ожидалось исключение {error.__name__} для имени {name}.'
                ):
                    self.manager_2count.find_medicine(name)

    def test_add_medicine(self):
        test_data = (
            (self.medicine_name_1, self.empty_manager),
            (self.medicine_name_2, self.manager_1count),
            (self.medicine_name_3, self.manager_2count),
        )

        for name, manager in test_data:
            with self.subTest(
                f'Проверка добавления лекарства: {name}.'
            ):
                start_count = len(manager._MedicineManager__medicines)
                manager.add_medicine(name)
                end_count = len(manager._MedicineManager__medicines)
                medicine = manager._MedicineManager__medicines[-1]

                self.assertEqual(
                    end_count - start_count, 1,
                    msg='Лекарство не было добавлено.'
                )
                self.assertEqual(
                    medicine.name, name,
                    msg=f'Ожидалось название {name}, но получено {medicine.name}.'
                )

    def test_add_medicine_with_uncorrect_data(self):
        for name, error, msg in self.test_uncorrect_data:
            start_count = len(self.empty_manager._MedicineManager__medicines)

            with self.subTest(msg=msg):
                with self.assertRaises(
                    error,
                    msg=f'Ожидалось исключение {error.__name__} для имени {name}.'
                ):
                    self.empty_manager.add_medicine(name)
            
            end_count = len(self.empty_manager._MedicineManager__medicines)
            self.assertEqual(
                end_count,
                start_count,
                msg='Количество лекарств не должно измениться при ошибке.'
            )

    def test_add_medicine_with_duplicate(self):
        test_data = self.medicine_name_1, self.medicine_name_2

        for name in test_data:
            with self.subTest(
                f'Проверка добавления дубликата для лекарства: {name}.'
            ):
                start_count = len(self.manager_2count._MedicineManager__medicines)
                
                with self.assertRaises(
                    ValueError,
                    msg=f'Ожидалось исключение ValueError для имени {name}.'
                ):
                    self.manager_2count.add_medicine(name)
                
                end_count = len(self.manager_2count._MedicineManager__medicines)
                self.assertEqual(
                    end_count,
                    start_count,
                    msg=f'Количество лекарств не должно измениться при добавлении дубликата {name}.'
                )

    def test_remove_medicine(self):
        test_data = (
            self.medicine_name_1,
            self.medicine_name_2
        )

        for name in test_data:
            with self.subTest(
                f'Проверка удаления лекарства: {name}.'
            ):
                start_count = len(self.manager_2count._MedicineManager__medicines)
                self.manager_2count.remove_medicine(name)
                end_count = len(self.manager_2count._MedicineManager__medicines)

                self.assertEqual(
                    start_count - end_count, 1,
                    msg='Лекарство не было удалено.'
                )


    def test_remove_medicine_with_uncorrect_data(self):
        for name, error, msg in self.test_uncorrect_data:
            start_count = len(self.empty_manager._MedicineManager__medicines)

            with self.subTest(msg=msg):
                with self.assertRaises(
                    error,
                    msg=f'Ожидалось исключение {error.__name__} для имени {name}.'
                ):
                    self.empty_manager.remove_medicine(name)
            
            end_count = len(self.empty_manager._MedicineManager__medicines)

            self.assertEqual(
                end_count,
                start_count,
                msg='Количество лекарств не должно измениться при ошибке.'
            )

    def test_remove_medicine_non_exist(self):
        start_count = len(self.manager_2count._MedicineManager__medicines)
        
        with self.assertRaises(
            ValueError,
            msg=f'При удалении несуществующего объекта ожидалось исключение ValueError.'
        ):
            self.manager_2count.remove_medicine(self.medicine_name_3)
        
        end_count = len(self.manager_2count._MedicineManager__medicines)

        self.assertEqual(
            end_count,
            start_count,
            msg=f'Количество лекарств не должно измениться при удалении несуществующего объекта.'
        )

    def test_edit_medicine(self):
        start_count = len(self.manager_1count._MedicineManager__medicines)
        self.manager_1count.edit_medicine(self.medicine_name_1, self.medicine_name_2)
        end_count = len(self.manager_1count._MedicineManager__medicines)
        medicine = self.manager_1count._MedicineManager__medicines[-1]

        self.assertEqual(
            medicine.name, self.medicine_name_2,
            msg=f'Ожидалось название {self.medicine_name_2}, но получено {medicine.name}.'
        )

        self.assertEqual(
            start_count, end_count,
            msg='При редактировании объекта изменилось количество объектов.'
        )

    def test_edit_medicine_with_uncorrect_data(self):
        for new_name, error, msg in self.test_uncorrect_data:
            start_count = len(self.manager_2count._MedicineManager__medicines)

            with self.subTest(msg=msg):
                with self.assertRaises(
                    error,
                    msg=f'Ожидалось исключение {error.__name__} для имени {new_name}.'
                ):
                    self.manager_2count.edit_medicine(self.medicine_name_1, new_name)
            
            end_count = len(self.manager_2count._MedicineManager__medicines)

            self.assertEqual(
                end_count,
                start_count,
                msg='Количество лекарств не должно измениться при ошибке.'
            )
    
    def test_edit_medicine_with_duplicate_name(self):
        test_data = (
            (self.medicine_name_1, self.medicine_name_2),
            (self.medicine_name_2, self.medicine_name_1)
        )

        for current_name, new_name in test_data:
            with self.subTest(
                f'Проверка редактирования на занятое имя {new_name} для лекарства: {current_name}.'
            ):
                start_count = len(self.manager_2count._MedicineManager__medicines)
                
                with self.assertRaises(
                    ValueError,
                    msg=f'Ожидалось исключение ValueError для имени {new_name}.'
                ):
                    self.manager_2count.edit_medicine(current_name, new_name)
                
                end_count = len(self.manager_2count._MedicineManager__medicines)

                self.assertEqual(
                    end_count,
                    start_count,
                    msg='Количество лекарств не должно измениться при редактировании.'
                )

    def test_edit_medicine_non_exist(self):
        start_count = len(self.manager_1count._MedicineManager__medicines)
        
        with self.assertRaises(
            ValueError,
            msg=f'При редактировании несуществующего объекта ожидалось исключение ValueError.'
        ):
            self.manager_1count.edit_medicine(self.medicine_name_2, self.medicine_name_3)
        
        end_count = len(self.manager_1count._MedicineManager__medicines)

        self.assertEqual(
            end_count,
            start_count,
            msg=f'Количество лекарств не должно измениться при редактировании несуществующего объекта.'
        )

    def test_get_medicines_list(self):
        medicines_str = f'1. {self.medicine_name_1}\n2. {self.medicine_name_2}'

        self.assertEqual(
            self.manager_2count.get_medicines_list(),
            medicines_str,
            msg=f'Получение строки списка лекарств не соответствует шаблону.\nШаблон:\n{medicines_str}'
        )
    
    def test_get_medicine_list_empty(self):
        empty_medicines_str = 'Список пуст!'

        self.assertEqual(
            self.empty_manager.get_medicines_list(),
            empty_medicines_str,
            msg=f'Получение строки при пустом списке лекарств не соответствует шаблону.\nШаблон:\n{empty_medicines_str}'
        )


if __name__ == '__main__':
    unittest.main()
