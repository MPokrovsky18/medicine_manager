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
        
        try:
            if user_input == '1':
                print(manager.get_medicines_list())
            elif user_input == '2':
                new_medicine_name = input('Введите название лекарства: ')

                if new_medicine_name:
                    manager.add_medicine(new_medicine_name)
                    print('Лекарство добавлено!')
                else:
                    print('Некорректный ввод!')
            elif user_input == '3':
                print(manager.get_medicines_list())
                target_medicine_name = input('Введите название лекарства: ')
                new_medicine_name = input('Новое название лекарства: ')

                if target_medicine_name and new_medicine_name:
                    manager.edit_medicine(target_medicine_name, new_medicine_name)
                    print('Лекарство изменено!')
                else:
                    print('Некорректный ввод!')
            elif user_input == '4':
                print(manager.get_medicines_list())
                target_medicine_name = input('Введите название лекарства: ')

                if target_medicine_name:
                    manager.remove_medicine(target_medicine_name)
                    print('Лекарство удалено!')
                else:
                    print('Некорректный ввод!')
            elif user_input == '0':
                is_run = False
            else:
                print('Некорректный ввод!')
        except Exception as e:
            print(e)

        print('\n------------------\n')


if __name__ == '__main__':
    console_app()
    print('Программа завершена!')
