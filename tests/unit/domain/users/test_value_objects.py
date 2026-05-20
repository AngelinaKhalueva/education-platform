import pytest

from domain.users.value_objects import Email, Password, UserRole


class TestEmail:
    """
    Тестирование Email.
    """

    def test_valid_email(self):
        """
        Правильный email создается без ошибок.
        """

        email = Email("test@example.com")
        assert email.value == "test@example.com"

    def test_invalid_email_no_at(self):
        """
        Email без @ вызывает ошибку.
        """

        with pytest.raises(ValueError, match="Некорректный email"):
            Email("invalid-email")

    def test_invalid_email_no_domain(self):
        """
        Email без домена вызывает ошибку.
        """

        with pytest.raises(ValueError, match="Некорректный email"):
            Email("test@")

    def test_invalid_email_empty(self):
        """
        Пустая строка вызывает ошибку.
        """

        with pytest.raises(ValueError, match="Некорректный email"):
            Email("")


class TestPassword:
    """
    Тестирование пароля.
    """

    def test_valid_password(self):
        """
        Правильный пароль создается без ошибок.
        """

        Password.validate("StrongPass1!")

    def test_too_short(self):
        """
        Пароль короче 8 символов вызывает ошибку.
        """

        with pytest.raises(ValueError, match="от 8 до 16"):
            Password.validate("Sh1!")

    def test_no_uppercase(self):
        """
        Пароль без буквы в верхнем регистре вызывает ошибку.
        """

        with pytest.raises(ValueError, match="заглавную"):
            Password.validate("weak_password1")

    def test_no_lowercase(self):
        """
        Пароль без буквы в нижнем регистре вызывает ошибку.
        """

        with pytest.raises(ValueError, match="строчную"):
            Password.validate("WEAK_PASSWORD1")

    def test_no_digit(self):
        """
        Пароль без цифр вызывает ошибку.
        """

        with pytest.raises(ValueError, match="цифру"):
            Password.validate("WeakPass!")

    def test_no_special_char(self):
        """
        Пароль без спецсимвола вызывает ошибку.
        """

        with pytest.raises(ValueError, match="спец"):
            Password.validate("WeakPass1")

    def test_too_long(self):
        """
        Пароль длиннее 16 символов вызывает ошибку.
        Максимальная длина превышена.
        """

        with pytest.raises(ValueError, match="от 8 до 16"):
            Password.validate("Very_long_password1!")


class TestUserRole:
    """
    Тестирование ролей.
    """

    def test_student_role_exists(self):
        """
        Роль STUDENT равна "student".
        """

        assert UserRole.STUDENT == "student"

    def test_mentor_role_exists(self):
        """
        Роль MENTOR равна "mentor".
        """

        assert UserRole.MENTOR == "mentor"

    def test_admin_role_exists(self):
        """
        Роль ADMIN равна "admin".
        """

        assert UserRole.ADMIN == "admin"

    def test_different_roles_not_equal(self):
        """
        Разные роли не равны друг другу.
        """

        assert UserRole.STUDENT != UserRole.MENTOR
