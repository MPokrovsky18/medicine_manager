from medicines.models import Drops, Pills


class MedicineFactory:
    """
    Класс, который создает новые лекарства.
    """

    @staticmethod
    def get_new_pills(*args, **kwargs):
        """
        Создать новый объект типа Pills.
        """
        return Pills(*args, **kwargs)

    @staticmethod
    def get_new_drops(*args, **kwargs):
        """
        Создать новый объект типа Drops.
        """
        return Drops(*args, **kwargs)
