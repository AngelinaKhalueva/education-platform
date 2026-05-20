# Образовательная платформа

**Стек:** Python 3.14, Django 6.0, DRF, PostgreSQL, Redis  
**Архитектура:** Onion Architecture + Domain-Driven Design  
**Разработчик:** Ангелина Халуева  

---

## Описание

Коммерческая образовательная платформа с подписками и геймификацией. Пользователи могут регистрироваться, покупать курсы, проходить уроки, сдавать домашние задания и отслеживать прогресс.

---

## Архитектура

Проект построен на принципах **Domain-Driven Design** и **Onion Architecture**.

### Слои

| Слой | Назначение |
|---|---|
| `domain/` | Чистая бизнес-логика (entities, value objects, aggregates) |
| `application/` | Сценарии использования (use cases, сервисы) |
| `infrastructure/` | Реализации (Django ORM, внешние API) |
| `presentation/` | REST API (DRF views, serializers) |

### Ограниченные контексты

| Контекст | Описание |
|---|---|
| `users` | Регистрация, аутентификация, профиль, роли |
| `courses` | Создание и управление курсами |
| `learning` | Прогресс обучения, домашние задания |
| `payments` | Оплата курсов, подписки |

---

## Установка

### Требования

- Python 3.14
- uv

### Запуск

```bash
# Клонировать репозиторий
git clone <url>
cd education-platform

# Установить зависимости
uv sync

# Применить миграции
python src/manage.py migrate

# Запустить сервер
python src/manage.py runserver
