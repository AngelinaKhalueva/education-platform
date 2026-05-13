# UserNotFoundError, EmailAlreadyExistsError
class UserNotFoundError(Exception):
    """
    Пользователь не найден.
    """

    pass


class EmailAlreadyExistsError(Exception):
    """
    Email уже зарегистрирован в системе.
    """


class TelegramAlreadyLinkedError(Exception):
    """
    Telegram уже привязан к другому аккаунту.
    """

    pass
