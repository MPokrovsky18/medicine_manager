import json
from os import makedirs
from os.path import dirname, exists

from medicines.serializers import JSONMedicineSerializer


class JSONStorageManager:
    """
    Класс для сохранения и загрузки данных json-файла.
    """

    def __init__(self, file_path: str):
        self._file_path = file_path
        self.__serializer = JSONMedicineSerializer()

    def save_data(self, data):
        """Сохранить данные в файл."""
        makedirs(dirname(self._file_path), exist_ok=True)
        json_data = self.__serializer.serialize(data)

        with open(self._file_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file)

    def load_data(self):
        """
        Загрузить данные из файла.
        """
        if exists(self._file_path):
            with open(self._file_path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
        else:
            json_data = {}

        return self.__serializer.deserialize(json_data)
