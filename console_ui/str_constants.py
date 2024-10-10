from config import APP_NAME
from medicines.managers import MEDICINES_ENUM


SPLIT_LINE = '------------------------------'

WELCOME_TEXT = f'''{SPLIT_LINE}
Добро пожаловать в приложение "{APP_NAME}"!
Приложение поможет вам следить за наличием лекарств,
их сроками годности и напомнит, когда нужно что-то купить или принять.
{SPLIT_LINE}
'''

START_ADD_NEW_MEDICINE_TEXT = f'''Добавление нового лекарства
Для отмены в любой момент введите "q"
{SPLIT_LINE}
'''

ENUM_MEDICINE_TYPES = (
    '\n'.join(
        f'{i} - {name}' for i, name in enumerate(MEDICINES_ENUM, 1)
    )
)
