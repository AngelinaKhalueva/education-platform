# IUserRepository
from abc import ABC, abstractmethod
from uuid import UUID

from domain.users.aggregates import UserAggregate
from domain.users.value_objects import Email


class IUserRepository(ABC):
    """
    Абстрактный интерфейс репозитория пользователей.
    Определяет контракт для доступа к данным.
    Прослойка между доменом и БД.
    Реализация в infrastructure/users/repositories.py
    """

    @abstractmethod
    def get_by_id(self, user_id: UUID) -> UserAggregate | None: ...

    @abstractmethod
    def get_by_email(self, email: Email) -> UserAggregate | None: ...

    @abstractmethod
    def save(self, user: UserAggregate) -> None: ...

    @abstractmethod
    def delete(self, user_id: UUID) -> None: ...
