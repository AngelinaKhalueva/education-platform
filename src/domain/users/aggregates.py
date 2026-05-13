# UserAggregate
from dataclasses import dataclass

from domain.users.entities import UserEntity
from domain.users.value_objects import Email


@dataclass
class UserAggregate:
    """
    Корень агрегата для контекста пользователя.
    Точка входа для всех изменений пользователя.
    """

    user: UserEntity

    def change_email(self, new_email: Email) -> None:
        """
        Изменение email пользователя.
        """
        if self.user.email == new_email:
            raise ValueError("Новый email должен отличаться от текущего.")
        self.user.email = new_email

    def link_telegram(self, telegram_id: str) -> None:
        """
        Делегирование проверки сущности.
        """
        self.user.link_telegram(telegram_id)


# TODO:
#  логика проверки подтверждения email перед заменой
#  логика отказа в удалении аккаунта с активной подпиской
#  привязывать Telegram можно только подтверждённым пользователям
