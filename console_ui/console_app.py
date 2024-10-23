from datetime import datetime

from console_ui.input_helpers import (
    gather_required_params,
    execute_action_if_confirmed,
    get_valid_input_or_cancel
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
        if self.__manager.get_medicines_by_filters(**kwargs):
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
            if required_arguments.get('current_quantity')
            else capacity
        )

        entered_data = f'''тип: {MEDICINES_ENUM[medicine_type][0]}
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

    def select_target_medicines(self):
        self.show_medicines()

        if self.__manager.medicine_count == 0:
            return None

        user_input = get_valid_input_or_cancel(
            input_message='Введите название лекарства или порядковый номер',
            validation_method=(
                lambda x:
                    not x.isdigit()
                    or x.isdigit()
                    and int(x) > 0
                    and int(x) <= self.__manager.medicine_count
            ),
            error_message='Команда должна быть числом из списка или текстом.'
        )

        if user_input == 'q':
            return None

        if user_input.isdigit():
            return self.__manager.get_medicines_by_filters()[
                int(user_input) - 1
            ]

        medicines = self.__manager.get_medicines_by_filters(
                title=user_input
            )

        if not medicines:
            print(f'Лекарство с именем {user_input} не найдено.')
            return None

        if len(medicines) == 1:
            return medicines[0]

        print('Найдено несколько упаковок:')
        self.show_medicines(medicines)
        user_input = get_valid_input_or_cancel(
            input_message='Введите номер упаковки или 0, чтобы выбрать все',
            validation_method=(
                lambda x:
                    x.isdigit()
                    and int(x) >= 0
                    and int(x) <= len(medicines)
            ),
            error_message='Команда должна быть числом из списка или 0.'
        )

        if user_input == 'q':
            return None

        if user_input == '0':
            return medicines

        return medicines[int(user_input) - 1]

    def remove_medicine(self) -> None:
        """
        Удалить лекарство.
        """
        print('Удаление лекарства:\n')

        target = self.select_target_medicines()

        if not target:
            return

        if isinstance(target, list):
            execute_action_if_confirmed(
                lambda x: [
                    self.__manager.remove_medicine(i.id) for i in x
                ],
                'Удалить все упаковки из списка?',
                target
            )
        else:
            execute_action_if_confirmed(
                question=f'{target}\nУдалить эту упаковку?',
                method=self.__manager.remove_medicine,
                id=target.id
            )

    def edit_medicine(self) -> None:
        """
        Редактировать лекарство.
        """
        print('Редактирование лекарства:\n')
        target = self.select_target_medicines()

        if not target:
            return

        if isinstance(target, list):
            print(
                'Для нескольких лекарств сразу можно изменить тип и название.'
                + 'Пропустите параметр, чтобы не менять.'
            )

            required_arguments = gather_required_params(
                True,
                'medicine_type', 'title'
            )

            if not required_arguments:
                return

            enter_index = required_arguments.get('medicine_type')
            medicine_type = int(enter_index) - 1 if enter_index else None
            title = required_arguments.get('title')

            execute_action_if_confirmed(
                lambda targets, **kwargs: [
                    self.__manager.edit_medicine(i.id, **kwargs)
                    for i in targets
                ],
                'Применить изменения ко всем упаковкам из списка?',
                target,
                medicine_type=medicine_type,
                title=title
            )
        else:
            print('Введите новые данные или пропустите параметр.')
            required_arguments = gather_required_params(
                default_can_empty_input=True
            )

            if not required_arguments:
                return

            medicine_type = required_arguments.get('medicine_type')
            title = required_arguments.get('title')
            expiration_date = required_arguments.get('expiration_date')
            capacity = required_arguments.get('capacity')
            current_quantity = required_arguments.get('current_quantity')

            medicine_type = int(medicine_type) - 1 if medicine_type else None
            expiration_date = datetime.strptime(
                expiration_date, '%d.%m.%Y'
            ).date() if expiration_date else target.expiration_date
            capacity = float(capacity) if capacity else target.capacity
            current_quantity = (
                float(current_quantity)
                if current_quantity
                else target.current_quantity
            )

            entered_data = f'''тип: {
                MEDICINES_ENUM[medicine_type][0]
                if medicine_type
                else 'не изменяем'
            }
название: {title or target.title}
срок годности: {datetime.strftime(expiration_date, '%d.%m.%Y')}
объём: {capacity}
текущее количество: {current_quantity}
'''

            confirmation_text = f'''Проверьте данные:
{entered_data}
{SPLIT_LINE}
Подтвердить изменение?'''

            execute_action_if_confirmed(
                self.__manager.edit_medicine,
                confirmation_text,
                id=target.id,
                medicine_type=medicine_type,
                title=title,
                expiration_date=expiration_date,
                capacity=capacity,
                current_quantity=current_quantity
            )

    def show_medicines(self, medicines: list = None) -> None:
        """
        Показать список лекарств.
        """
        if not medicines:
            medicines = self.__manager.get_medicines_by_filters()

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
                try:
                    _, action = command
                    action()
                except Exception as e:
                    print('\nОперация не выполнена!')
                    print(e)
            else:
                print('Некорректный ввод!')

            print(SPLIT_LINE)
