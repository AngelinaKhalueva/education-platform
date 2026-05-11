# Техническое задание: Образовательная платформа

## 1. Общее описание

**Тип:** Коммерческая образовательная платформа  
**Архитектура:** Modular Monolith (Onion Architecture + DDD)  
**Стек:** Django 6 + DRF + PostgreSQL + Redis  
**Цель:** Портфолио-grade проект с разделением на слои и Bounded Contexts  

---

## 2. Bounded Contexts

### 2.1 users — Учётные записи
Регистрация, аутентификация, профиль, роли.

**Задачи:**
- [ ] Регистрация по email и паролю
- [ ] JWT-аутентификация (access + refresh токены)
- [ ] Три роли: student, mentor, admin
- [ ] Личный кабинет (профиль, смена пароля)
- [ ] Привязка Telegram-аккаунта (позже)

### 2.2 courses — Управление курсами
Создание и хранение контента курсов.

**Задачи:**
- [ ] CRUD курсов (admin/mentor)
- [ ] Модули и уроки внутри курса
- [ ] Типы контента: видео, текст, код, изображения
- [ ] Публикация курса (draft → published)

### 2.3 learning — Процесс обучения
Прогресс пользователя, прохождение уроков, домашние задания.

**Задачи:**
- [ ] Отслеживание прогресса по урокам
- [ ] Стейт-машина: locked → available → in_progress → completed
- [ ] Открытие уроков по порядку (нельзя перескочить)
- [ ] Сдача домашних заданий
- [ ] Проверка ДЗ ментором

### 2.4 payments — Платежи и подписки
Оплата курсов, управление подписками.

**Задачи:**
- [ ] Разовая покупка курса
- [ ] Подписка (ежемесячная)
- [ ] Интеграция с ЮKassa
- [ ] Атомарная активация доступа после оплаты
- [ ] Напоминание об истечении подписки

---

## 3. Слои архитектуры

### 3.1 domain/
Чистая бизнес-логика. Без Django, без БД.  
Файлы: entities, value_objects, aggregates, repositories (интерфейсы), exceptions.

### 3.2 application/
Сценарии использования (use cases). Оркестрация.  
Файлы: services, use_cases, interfaces (порты), events.

### 3.3 infrastructure/
Реализации: Django ORM, ЮKassa, Unisender.  
Файлы: models, repositories (реализации), adapters.

### 3.4 presentation/
REST API. DRF views, serializers, urls.

---

## 4. Порядок разработки

### Этап 1: users
- domain: UserEntity, Email, UserRole, UserAggregate
- application: RegisterUseCase, LoginUseCase
- infrastructure: UserModel, DjangoUserRepository
- presentation: RegisterView, LoginView

### Этап 2: courses
- domain: Course, Module, Lesson, CourseAggregate
- application: CreateCourseUseCase, PublishCourseUseCase
- infrastructure: CourseModel, ModuleModel, LessonModel
- presentation: CourseListView, CourseDetailView

### Этап 3: learning
- domain: EnrollmentAggregate, LessonProgress, стейт-машина
- application: StartLessonUseCase, CompleteLessonUseCase
- infrastructure: EnrollmentModel, LessonProgressModel
- presentation: ProgressView, SubmitHomeworkView

### Этап 4: payments
- domain: Invoice, Money, InvoiceAggregate
- application: ProcessPaymentUseCase
- infrastructure: InvoiceModel, YooKassaAdapter
- presentation: PaymentWebhookView

### Этап 5: Интеграция
- payments → learning (оплата активирует доступ)
- События: SubscriptionActivated, LessonCompleted

---

## 5. Тестирование

- Unit: доменный слой (pytest)
- Integration: application + infrastructure (pytest + test DB)
- E2E: критический путь «регистрация → оплата → доступ → урок»

---

## 6. Безопасность

- [ ] JWT RS256 (асимметричные ключи)
- [ ] RBAC (student/mentor/admin)
- [ ] Защита от IDOR
- [ ] Rate limiting
- [ ] Валидация загружаемых файлов
- [ ] Аудит действий

---

## 7. Отложено

- [ ] Telegram-бот (ежедневные тесты)
- [ ] Code Runner (изолированное выполнение кода)
- [ ] Мобильное приложение
- [ ] Версионирование контента
- [ ] Аналитика