## domain/courses/

### entities.py
Сущности с уникальным ID:
- `Course` — id, title, description, status (draft/published)
- `Module` — id, course_id, title, order
- `Lesson` — id, module_id, title, content_type (video/text/quiz), content_data

### value_objects.py
Неизменяемые объекты без ID:
- `ContentType` — "video" | "text" | "quiz"
- `LessonOrder` — порядковый номер урока в модуле

### aggregates.py
Корень агрегата:
- `CourseAggregate` — содержит Course + список Module (каждый Module содержит список Lesson). Методы: `add_module()`, `publish()`. Инвариант: нельзя опубликовать пустой курс.

### repositories.py
Абстракции:
- `ICourseRepository` — методы `get_by_id()`, `save()`, `list_published()`

### exceptions.py
- `CourseNotPublishedError`
- `ModuleEmptyError`

---

## application/courses/

### services.py
Оркестрация:
- `CourseService` — вызывает репозиторий, UoW, доменные методы. Не содержит бизнес-логики.

### use_cases.py
Сценарии:
- `CreateCourseUseCase` — создать курс
- `AddModuleUseCase` — добавить модуль
- `PublishCourseUseCase` — опубликовать курс

---

## infrastructure/courses/

### models.py
Таблицы Django ORM:
- `CourseModel` — id, title, description, status, version
- `ModuleModel` — id, course (FK), title, order
- `LessonModel` — id, module (FK), title, content_type, content_data (JSONField)

### repositories.py
Реализации:
- `DjangoCourseRepository` — имплементирует `ICourseRepository`, маппит ORM-модели ↔ доменные сущности

---

## presentation/courses/

### serializers.py
DRF сериализаторы:
- `CourseSerializer` — id, title, description, modules
- `LessonSerializer` — id, title, content_type

### views.py
API:
- `CourseListView` — GET список курсов
- `CourseDetailView` — GET курс + модули + уроки

### urls.py
Маршруты:
- `/courses/` → CourseListView
- `/courses/<id>/` → CourseDetailView
