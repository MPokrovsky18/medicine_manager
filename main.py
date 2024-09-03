class Medicine:
    def __init__(self, name) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

medicines = []


def add_medicine(medicine: Medicine) -> bool:
    if medicine:
        medicines.append(medicine)
        return True

    return False


def delete_medicine(medicine_id: int) -> bool:
    if medicine_id >= 0 and medicine_id < len(medicines):
        medicines.pop(medicine_id)
        return True

    return False


def edit_medicine(medicine_id: int, name: str) -> bool:
    if name and medicine_id >= 0 and medicine_id < len(medicines):
        medicines[medicine_id].name = name
        return True
    
    return False


def get_medicines_list() -> str:
    if medicines:
        return '\n'.join(
            f'{index}. {medicine.name}' for index, medicine in enumerate(medicines)
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
                edit_medicine(int(target_medicine_id), new_medicine_name.lower())
                print('Лекарство изменено!')
            else:
                print('Некорректный ввод!')
        elif user_input == '4':
            print(get_medicines_list())
            target_medicine_id = input('Введите номер лекарства: ')

            if target_medicine_id.isdigit():
                is_delete = delete_medicine(int(target_medicine_id))

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


console_app()
print('Программа завершена!')