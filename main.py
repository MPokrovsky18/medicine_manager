class Medicine:
    def __init__(self, name) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name


medicines: list[Medicine] = []


def add_medicine(medicine: Medicine, medicine_list: list[Medicine] = medicines) -> bool:
    if medicine:
        medicine_list.append(medicine)
        return True

    return False


def remove_medicine(medicine_id: int, medicine_list: list[Medicine] = medicines) -> bool:
    if medicine_id >= 0 and medicine_id < len(medicine_list):
        medicine_list.pop(medicine_id)
        return True

    return False


def edit_medicine(medicine_id: int, name: str, medicine_list: list[Medicine] = medicines) -> bool:
    if name and medicine_id >= 0 and medicine_id < len(medicine_list):
        medicine_list[medicine_id].name = name
        return True
    
    return False


def get_medicines_list(medicine_list: list[Medicine] = medicines) -> str:
    if medicine_list:
        return '\n'.join(
            f'{index}. {medicine.name}' for index, medicine in enumerate(medicine_list)
        )
    
    return 'Список пуст!'


def show_menu() -> None:
    print('Меню:')
    print('1. Все лекарства')
    print('2. Добавить лекарство')
    print('3. Редактировать лекарство')
    print('4. Удалить лекарство')
    print('0. Выйти из программы')


def console_app() -> None:
    is_run = True

    while is_run:
        show_menu()
        user_input = input('Выберите пункт меню: ')
        print('\n------------------\n')

        if user_input == '1':
            print(get_medicines_list())
        elif user_input == '2':
            new_medicine_name = input('Введите название лекарства: ')

            if new_medicine_name:
                add_medicine(Medicine(new_medicine_name.lower()))
                print('Лекарство добавлено!')
            else:
                print('Некорректный ввод!')
        elif user_input == '3':
            print(get_medicines_list())
            target_medicine_id = input('Введите номер лекарства: ')
            new_medicine_name = input('Введите название лекарства: ')

            if target_medicine_id.isdigit() and new_medicine_name:
                is_edit = edit_medicine(int(target_medicine_id), new_medicine_name.lower())

                if is_edit:
                    print('Лекарство изменено!')
                else:
                    print(f'Лекарство под номером {target_medicine_id} не найдено.')
            else:
                print('Некорректный ввод!')
        elif user_input == '4':
            print(get_medicines_list())
            target_medicine_id = input('Введите номер лекарства: ')

            if target_medicine_id.isdigit():
                is_delete = remove_medicine(int(target_medicine_id))

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
