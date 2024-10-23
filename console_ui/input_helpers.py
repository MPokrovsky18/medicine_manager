from console_ui.validators import isfloat, validate_str_format_for_date
from console_ui.str_constants import SPLIT_LINE, ENUM_MEDICINE_TYPES
from medicines.managers import MEDICINES_ENUM


def get_valid_input_or_cancel(
    input_message: str,
    validation_method=None,
    error_message: str = None,
    can_empty_input: bool = False
) -> str | None:
    """
    Получить от пользователя корректные данные из консоли.
    """
    user_input = None
    is_valid_input = False

    while not is_valid_input:
        user_input = input(input_message + ' (или "q" для отмены): ')

        if can_empty_input and not user_input:
            return None

        if not user_input:
            print(SPLIT_LINE)
            print('Строка не должна быть пустой.')
        elif user_input.lower() in ('q', 'й'):
            print(SPLIT_LINE)
            print('Операция прервана.')
            return 'q'
        elif validation_method and not validation_method(user_input):
            print(SPLIT_LINE)
            print(error_message)
        else:
            is_valid_input = True

        print(SPLIT_LINE)

    return user_input


def get_all_parameters_with_input_conditions():
    """
    Возвращает словарь с параметрами и условиями их получения от пользователя.
    """
    return {
        'medicine_type': {
            'input_message': (
                'Выберите тип лекарства:\n'
                + ENUM_MEDICINE_TYPES
                + '\n'
                + 'Введите команду'
            ),
            'validation_method': (
                lambda x: x.isdigit()
                and int(x) > 0
                and int(x) - 1 < len(MEDICINES_ENUM)
            ),
            'error_message': 'Команда должна быть числом из списка типов.',
        },
        'title': {
            'input_message': 'Введите название лекарства',
            'validation_method': lambda x: len(x) >= 3 and len(x) < 50,
            'error_message': (
                'Длина названия должна быть не менее 3-х символов '
                + 'и не более 50-ти.'
            ),
        },
        'expiration_date': {
            'input_message': 'Введите срок годности (ДД.ММ.ГГГГ)',
            'validation_method':
                validate_str_format_for_date,
            'error_message': 'Неверный формат даты.',
        },
        'capacity': {
            'input_message': 'Введите объём лекарства',
            'validation_method': lambda x: isfloat(x) and float(x) > 0,
            'error_message': 'Объём должен быть положительным числом.',
        },
        'current_quantity': {
            'input_message':
                'Введите количество (оставьте пустым, если упаковка полная)',
            'validation_method':
                lambda x: (isfloat(x) and float(x) >= 0) or not x,
            'error_message':
                'Введите положительное число или оставьте поле пустым.',
            'can_empty_input': True
        }
    }


def gather_required_params(default_can_empty_input=False, *params_names):
    """
    Получить от пользователя значения для необходимых аргументов.
    """
    all_required_arguments = get_all_parameters_with_input_conditions()

    params_keys_values = (
        dict.fromkeys(params_names)
        if params_names
        else dict.fromkeys(all_required_arguments.keys())
    )

    for arg_name, argument_data in all_required_arguments.items():
        if arg_name in params_keys_values:
            user_input = get_valid_input_or_cancel(
                input_message=argument_data['input_message'],
                validation_method=argument_data['validation_method'],
                error_message=argument_data['error_message'],
                can_empty_input=argument_data.get(
                    'can_empty_input', default_can_empty_input
                )
            )

            if user_input == 'q':
                return None

            if user_input:
                params_keys_values[arg_name] = user_input

    return params_keys_values


def execute_action_if_confirmed(
    method: callable, question: str, *args, **kwargs
) -> None:
    """
    Выполнить метод, если пользователь подтвердил.
    """
    user_input = input(question + '(y/n)(д/н): ').lower()

    if user_input in ('y', 'д', ''):
        method(*args, **kwargs)
        print('Операция выполнена!')
    else:
        print('Операция отменена!')
