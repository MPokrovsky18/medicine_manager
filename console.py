from config import APP_NAME
from medicines.managers import MedicineManager


APP_NAME = APP_NAME
SPLIT_LINE = '------------------'
MENU_ORDER = 'S', 'A', 'E', 'D', 'Q'


class ConsoleApp:
    """
    Представление консольного интерфейса.
    """

    def __init__(self, manager: MedicineManager = None) -> None:
        self.__commands = {
            'Q': ('Выйти из программы', self.quit),
            'Й': ('Выйти из программы', self.quit),
            'A': ('Добавить лекарство', self.add_medicine),
            'Ф': ('Добавить лекарство', self.add_medicine),
            'E': ('Редактировать лекарство', self.edit_medicine),
            'У': ('Редактировать лекарство', self.edit_medicine),
            'D': ('Удалить лекарство', self.remove_medicine),
            'В': ('Удалить лекарство', self.remove_medicine),
            'S': ('Показать все лекарства', self.show_medicines),
            'Ы': ('Показать все лекарства', self.show_medicines),
        }
        self.__menu = '\n'.join(
            f' - {self.__commands[command][0]} - {command}'
            for command in MENU_ORDER
        )

        if not manager:
            self.__manager = MedicineManager()
        else:
            self.__manager = manager

    def start(self):
        """
        Старт консольной программы.
        """
        print('Программа запущена...\n' + SPLIT_LINE)
        print(f'Добро пожаловать в приложение "{APP_NAME}"')
        print(SPLIT_LINE)

        self.__is_run = True
        self.run()

        print('Программа завершена!')

    def show_menu(self) -> None:
        """
        Вывести меню.
        """
        print('Меню:\n')
        print(self.__menu)
        print(SPLIT_LINE)

    def execute_if_confirmed(
        self, method: callable, question: str, *args
    ) -> None:
        """
        Выполнить метод, если пользователь подтвердил ввод.
        """
        user_input = input(question + '(y/n)(д/н): ').lower()

        if user_input in ('y', 'д', ''):
            method(*args)
            print('Операция выполнена!')
        else:
            print('Операция отменена!')

    def add_medicine(self) -> None:
        """
        Добавить лекарство.
        """
        print('Добавление лекарства:\n')
        new_medicine_name = input('Введите название: ')

        if new_medicine_name:
            self.execute_if_confirmed(
                self.__manager.add_medicine,
                f'Добавить "{new_medicine_name}" в список лекарств?',
                new_medicine_name
            )
        else:
            print('Некорректный ввод.')

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
        Показать список лекарств."""
        print(self.__manager.get_medicines_list())
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
            self.show_menu()
            user_input = input('Введите команду: ').upper()
            print(SPLIT_LINE)

            command = self.__commands.get(user_input)

            if command:
                try:
                    _, action = command
                    action()
                except Exception as e:
                    print('\nОперация не выполнена!')
                    print(e)
            else:
                print('Некорректный ввод!')

            print(SPLIT_LINE)
