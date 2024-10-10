from datetime import datetime

from console_ui.input_helpers import (
    gather_required_params, execute_action_if_confirmed
)
from console_ui.str_constants import (
    SPLIT_LINE, WELCOME_TEXT, START_ADD_NEW_MEDICINE_TEXT
)
from medicines.managers import MedicineManager, MEDICINES_ENUM


class ConsoleApp:
    """
    Представление консольного интерфейса.
    """

    def __init__(self, manager: MedicineManager = None) -> None:
        self.__commands = {
            '1': ('Посмотреть все лекарства', self.show_medicines),
            '2': ('Добавить новое лекарство', self.add_medicine),
            '3': ('Изменить данные о лекарстве', self.edit_medicine),
            '4': ('Удалить лекарство', self.remove_medicine),
            '5': ('Выйти из программы', self.quit),
        }
        self.__menu = '\n'.join(
            f'{command} - {description[0]}'
            for command, description in self.__commands.items()
        )

        self.__manager = manager if manager else MedicineManager()

    def start(self):
        """
        Старт консольной программы.
        """
        print('Программа запущена...\n')
        print(WELCOME_TEXT)

        self.__is_run = True
        self.run()

        print('Программа завершена!')

    def show_main_menu(self) -> None:
        """
        Вывести меню.
        """
        print('Главное меню:')
        print(self.__menu)
        print(SPLIT_LINE)

    def check_duplicates_and_confirm(self, *args, **kwargs) -> bool:
        """
        Проверяет наличие дубликатов лекарства
        и запрашивает подтверждение на добавление.
        """
        if self.__manager.get_duplicates(**kwargs):
            print('Лекарство с такими параметрами уже существует в аптечке.')

            confirmation = input(
                'Добавить ещё одну такую же упаковку?(y/n)(д/н): '
            )

            if confirmation.lower() in ('n', 'н'):
                print('Операция прервана!')
                return False

        return True

    def add_medicine(self) -> None:
        """
        Добавить лекарство.
        """
        print(START_ADD_NEW_MEDICINE_TEXT)

        required_arguments = gather_required_params()

        if not required_arguments:
            return

        medicine_type = int(required_arguments['medicine_type']) - 1
        title = required_arguments['title']
        expiration_date = datetime.strptime(
            required_arguments['expiration_date'], '%d.%m.%Y'
        ).date()
        capacity = float(required_arguments['capacity'])
        current_quantity = (
            float(required_arguments['current_quantity'])
            if required_arguments['current_quantity']
            else capacity
        )

        entered_data = f'''тип: {MEDICINES_ENUM[medicine_type]}
название: {title}
срок годности: {datetime.strftime(expiration_date, '%d.%m.%Y')}
объём: {capacity}
текущее количество: {current_quantity}
'''
        if self.check_duplicates_and_confirm(
            type_index=medicine_type,
            title=title,
            expiration_date=expiration_date,
            capacity=capacity,
            current_quantity=current_quantity
        ):
            confirmation_text = f'''Проверьте данные:
    {entered_data}
    {SPLIT_LINE}
    Подтвердить добавление?'''

            execute_action_if_confirmed(
                self.__manager.add_medicine,
                confirmation_text,
                medicine_type=medicine_type,
                title=title,
                expiration_date=expiration_date,
                capacity=capacity,
                current_quantity=current_quantity
            )

    def remove_medicine(self) -> None:
        """
        Удалить лекарство.
        """
        print('Удаление лекарства:\n')
        self.show_medicines()
        target_medicine_name = input('Введите название лекарства: ')

        if target_medicine_name:
            self.execute_if_confirmed(
                self.__manager.remove_medicine,
                f'Удалить "{target_medicine_name}" из списка лекарств?',
                target_medicine_name
            )
        else:
            print('Некорректный ввод.')

    def edit_medicine(self) -> None:
        """
        Редактировать лекарство.
        """
        print(self.__manager.get_medicines_list())
        target_medicine_name = input('Введите название лекарства: ')
        new_medicine_name = input('Новое название лекарства: ')

        if target_medicine_name and new_medicine_name:
            self.execute_if_confirmed(
                self.__manager.edit_medicine,
                f'Изменить "{target_medicine_name}" на "{new_medicine_name}"?',
                target_medicine_name,
                new_medicine_name
            )
        else:
            print('Некорректный ввод.')

    def show_medicines(self) -> None:
        """
        Показать список лекарств.
        """
        medicines = self.__manager.get_medicines_list()

        if medicines:
            print('Список лекарств: ')
            print(
                '\n'.join(
                    f'{i} - {medicine}'
                    for i, medicine in enumerate(medicines, 1)
                )
            )
        else:
            print('Список лекарств пуст!')

        print(SPLIT_LINE)

    def quit(self) -> None:
        """
        Завершить работу программы.
        """
        self.__is_run = False

    def run(self) -> None:
        """
        Запустить программу в консоли.
        """
        while self.__is_run:
            self.show_main_menu()
            user_input = input('Введите номер действия: ')
            print(SPLIT_LINE)

            command = self.__commands.get(user_input)

            if command:
                # try:
                _, action = command
                action()
                # except Exception as e:
                #     print('\nОперация не выполнена!')
                #     print(e)
            else:
                print('Некорректный ввод!')

            print(SPLIT_LINE)
