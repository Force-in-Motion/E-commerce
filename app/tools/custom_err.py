class DatabaseError(Exception):
    """Ошибка работы с базой данных."""

    pass


class NotFoundError(Exception):
    """Ошибка нахождения элемента."""

    pass
