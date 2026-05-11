from dataclasses import dataclass
import re
from enum import Enum


@dataclass(frozen=True)
class Email:
    """
    Email с валидацией.
    Неизменяемая сущность.
    """

    value: str

    PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    def __post_init__(self) -> None:
        if not re.match(self.PATTERN, self.value):
            raise ValueError(f"Некорректный email: {self.value}.")


@dataclass(frozen=True)
class Password:
    """
    Логика сложности пароля.
    Не хранит сам пароль.
    """

    MIN_LENGTH = 8
    MAX_LENGTH = 16

    @staticmethod
    def validate(raw_password: str) -> None:
        if (
            len(raw_password) < Password.MIN_LENGTH
            or len(raw_password) > Password.MAX_LENGTH
        ):
            raise ValueError(
                f"Пароль должен быть от {Password.MIN_LENGTH} до {Password.MAX_LENGTH} символов."
            )
        if not any(char.isupper() for char in raw_password):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву.")
        if not any(char.islower() for char in raw_password):
            raise ValueError("Пароль должен содержать хотя бы одну строчную букву.")
        if not any(char.isdigit() for char in raw_password):
            raise ValueError("Пароль должен содержать хотя бы одну цифру.")
        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for char in raw_password):
            raise ValueError("Пароль должен содержать хотя бы один спец. символ.")


class UserRole(str, Enum):
    """
    Допустимые роли.
    """

    STUDENT = "student"
    MENTOR = "mentor"
    ADMIN = "admin"
