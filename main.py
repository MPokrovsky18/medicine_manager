from medicine import Medicine, MedicineManager


def show_menu() -> None:
    """
    Вывести меню.
    """
    print('Меню:')
    print('1. Все лекарства')
    print('2. Добавить лекарство')
    print('3. Редактировать лекарство')
    print('4. Удалить лекарство')
    print('0. Выйти из программы')


def console_app() -> None:
    """
    Запустить программу в консоли.
    """
    is_run = True
    manager = MedicineManager()

    while is_run:
        show_menu()
        user_input = input('Выберите пункт меню: ')
        print('\n------------------\n')

        if user_input == '1':
            print(manager.get_medicines_list())
        elif user_input == '2':
            new_medicine_name = input('Введите название лекарства: ')

            if new_medicine_name:
                manager.add_medicine(Medicine(new_medicine_name.lower()))
                print('Лекарство добавлено!')
            else:
                print('Некорректный ввод!')
        elif user_input == '3':
            print(manager.get_medicines_list())
            target_medicine_id = input('Введите номер лекарства: ')
            new_medicine_name = input('Введите название лекарства: ')

            if target_medicine_id.isdigit() and new_medicine_name:
                is_edit = manager.edit_medicine(int(target_medicine_id), new_medicine_name.lower())

                if is_edit:
                    print('Лекарство изменено!')
                else:
                    print(f'Лекарство под номером {target_medicine_id} не найдено.')
            else:
                print('Некорректный ввод!')
        elif user_input == '4':
            print(manager.get_medicines_list())
            target_medicine_id = input('Введите номер лекарства: ')

            if target_medicine_id.isdigit():
                is_delete = manager.remove_medicine(int(target_medicine_id))

                if is_delete:
                    print('Лекарство удалено!')
                else:
                    print(f'Лекарство под номером {target_medicine_id} не найдено.')
            else:
                print('Некорректный ввод!')
        elif user_input == '0':
            is_run = False
        else:
            print('Некорректный ввод!')

        print('\n------------------\n')


if __name__ == '__main__':
    console_app()
    print('Программа завершена!')
