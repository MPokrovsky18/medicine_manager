from config import JSON_FILE_PATH
from console import ConsoleApp
from medicines.managers import MedicineManager
from storage import JSONStorageManager


class MedicineApp:
    """
    Представление главного приложения.
    """

    def __init__(self) -> None:
        self.__storage = JSONStorageManager(JSON_FILE_PATH)
        saved_data = self.__storage.load_data()
        self.__manager = MedicineManager(saved_data)
        self.__app = ConsoleApp(self.__manager)
    
    def run(self):
        """
        Запустить приложение.
        """
        try:
            self.__app.start()
        except Exception as e:
            print(f'Ошибка: {e}')
        finally:
            self.__storage.save_data(self.__manager.medicines)
            print('Данные сохранены.')
