# UserEntity (id, email, role)
from dataclasses import dataclass
from uuid import UUID

from domain.users.value_objects import Email, UserRole


@dataclass
class UserEntity:
    """
    Пользователь
    """

    id: UUID
    email: Email
    password_hash: str
    role: UserRole
    telegram_id: str | None = None
    _version: int = 1

    def link_telegram(self, telegram_id: str) -> None:
        """
        Привязка аккаунта telegram.
        """
        if self.telegram_id is not None:
            raise ValueError("Telegram уже привязан")
        self.telegram_id = telegram_id
