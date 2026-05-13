## Этап 1: users — Учётные записи

### Шаг 1. domain/users/value_objects.py

Создать объекты-значения:
- `Email` — строка с валидацией (регулярка)
- `Password` — строка, политика сложности (мин. 12 символов, заглавная, цифра, спецсимвол)
- `UserRole` — enum: `student`, `mentor`, `admin`

Объекты неизменяемые, без ID.

---

### Шаг 2. domain/users/entities.py

Создать сущность:
- `UserEntity` — поля: `id` (UUID), `email` (Email), `password_hash` (str), `role` (UserRole), `telegram_id` (опционально)

Сущность с уникальным `id`.

---

### Шаг 3. domain/users/aggregates.py

Создать агрегат:
- `UserAggregate` — корень: `UserEntity`
- Методы: `link_telegram(telegram_id)` — бизнес-правило: нельзя привязать Telegram дважды

---

### Шаг 4. domain/users/exceptions.py

Создать доменные ошибки:
- `EmailAlreadyExistsError`
- `UserNotFoundError`
- `TelegramAlreadyLinkedError`

---

### Шаг 5. domain/users/repositories.py

Создать абстрактный интерфейс:
- `IUserRepository` — методы: `get_by_id(id)`, `get_by_email(email)`, `save(user)`, `delete(user)`

ABC-класс, без реализации.

---

### Шаг 6. Написать unit-тесты для domain/users

Проверить:
- Email валидацию (правильный email, неправильный)
- UserRole enum (три значения)
- UserAggregate.link_telegram (первый раз ок, второй — ошибка)

---

### Шаг 7. application/users/interfaces.py

Создать порты для внешних зависимостей:
- `IHasher` — методы: `hash(password)`, `verify(password, hash)`
- `ITokenService` — методы: `generate(user)`, `validate(token)`

ABC-классы.

---

### Шаг 8. application/users/dto.py

Создать DTO:
- `RegisterDTO` — поля: `email`, `password`, `role`
- `LoginDTO` — поля: `email`, `password`
- `UserDTO` — поля: `id`, `email`, `role` (то, что возвращаем клиенту)
- `TokenPairDTO` — поля: `access`, `refresh`

Pydantic-модели.

---

### Шаг 9. application/users/use_cases.py

Создать сценарии:
- `RegisterUseCase` — шаги:
  1. Создать Email из DTO
  2. Проверить через репозиторий, что email не занят
  3. Создать UserAggregate
  4. Захэшировать пароль через IHasher
  5. Сохранить через репозиторий
  6. Вернуть UserDTO

- `LoginUseCase` — шаги:
  1. Найти пользователя по email через репозиторий
  2. Проверить пароль через IHasher
  3. Сгенерировать токены через ITokenService
  4. Вернуть TokenPairDTO

---

### Шаг 10. application/users/services.py

Создать сервис:
- `AccountService` — оркестрирует use cases, принимает через конструктор: `IUserRepository`, `IHasher`, `ITokenService`

---

### Шаг 11. Написать unit-тесты для application/users

Проверить:
- RegisterUseCase с мок-репозиторием (успех, email уже занят)
- LoginUseCase с мок-репозиторием (успех, неверный пароль)

---

### Шаг 12. infrastructure/users/models.py

Создать Django-модель:
- `UserModel` — поля: `id` (UUIDField PK), `email` (EmailField unique), `password` (CharField), `role` (CharField choices), `telegram_id` (CharField null), `version` (IntegerField)

---

### Шаг 13. infrastructure/users/repositories.py

Создать реализацию:
- `DjangoUserRepository` — имплементирует `IUserRepository`, маппит `UserModel` ↔ `UserAggregate`

---

### Шаг 14. infrastructure/users/hasher.py

Создать реализацию:
- `BcryptHasher` или `DjangoHasher` — имплементирует `IHasher`

---

### Шаг 15. infrastructure/users/token_service.py

Создать реализацию:
- `JWTTokenService` — имплементирует `ITokenService`, RS256, access на 15 мин, refresh на 7 дней

---

### Шаг 16. Написать интеграционные тесты для infrastructure/users

Проверить:
- DjangoUserRepository: save и get_by_email с тестовой БД
- BcryptHasher: hash + verify
- JWTTokenService: generate + validate

---

### Шаг 17. presentation/users/serializers.py

Создать DRF-сериализаторы:
- `RegisterSerializer` — принимает email, password, role
- `LoginSerializer` — принимает email, password
- `UserSerializer` — отдаёт id, email, role

---

### Шаг 18. presentation/users/views.py

Создать DRF-views:
- `RegisterView` — POST, вызывает `AccountService.register()`
- `LoginView` — POST, вызывает `AccountService.login()`
- `ProfileView` — GET, отдаёт текущего пользователя

---

### Шаг 19. presentation/users/urls.py

Создать маршруты:
- `POST /register/` → RegisterView
- `POST /login/` → LoginView
- `GET /me/` → ProfileView

---

### Шаг 20. Подключить urls в presentation/urls.py

```python
urlpatterns = [
    path('users/', include('presentation.users.urls')),
]
```

---

### Шаг 21. Проверить через curl или браузер

```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ -d '{"email":"test@test.com","password":"StrongPass1!","role":"student"}'
```
