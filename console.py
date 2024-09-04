from medicine import MedicineManager


APP_NAME = 'Лекарственный менеджер'
SPLIT_LINE = '------------------'
MENU = (
    ('S', 'Показать все лекарства'),
    ('A', 'Добавить лекарство'),
    ('E', 'Редактировать лекарство'),
    ('D', 'Удалить лекарство'),
    ('Q', 'Выйти из программы')
)

class ConsoleApp:
    """
    Представление консольного интерфейса.
    """
    def __init__(self) -> None:
        self.__menu = '\n'.join(f' - {description} - {command}' for command, description in MENU)
        self.__manager = MedicineManager()

    def start(self):
        """
        Старт консольной программы.
        """
        print('Программа запущена...\n' + SPLIT_LINE)
        print(f'Добро пожаловать в приложение "{APP_NAME}"')
        print(SPLIT_LINE)

        self.run()

        print('Программа завершена!')

    def show_menu(self) -> None:
        """
        Вывести меню.
        """
        print('Меню:\n')
        print(self.__menu)
        print(SPLIT_LINE)

    def execute_if_confirmed(self, method: callable, question: str, *args) -> None:
        """
        Выполнить метод, если пользователь подтвердил ввод.
        """
        user_input = input(question + '(y/n)(д/н): ').lower()

        if user_input in ('y', 'д'):
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

    def run(self) -> None:
        """
        Запустить программу в консоли.
        """
        is_run = True

        while is_run:
            self.show_menu()
            user_input = input('Введите команду: ').upper()
            print(SPLIT_LINE)
            
            try:
                if user_input in ('S', 'Ы'):
                    self.show_medicines()
                elif user_input in ('A', 'Ф'):
                    self.add_medicine()
                elif user_input in ('E', 'У'):
                    self.edit_medicine()
                elif user_input in ('D', 'В'):
                    self.remove_medicine()
                elif user_input in ('Q', 'Й'):
                    is_run = False
                else:
                    print('Некорректный ввод!')
            except Exception as e:
                print('\nОперация не выполнена!')
                print(e)

            print(SPLIT_LINE)
