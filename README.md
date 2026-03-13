# College TODO

Учебный проект на FastAPI: список задач с заметками, простая веб‑страница и авторизация (JWT + Google OAuth).

**Стек**
- FastAPI + Uvicorn
- PostgreSQL
- SQLAlchemy + Alembic
- Jinja2 (серверный UI)

**Ключевые возможности**
- CRUD задач
- Заметки к задачам (файлы в папке `notes`)
- Авторизация по логину/паролю
- Вход через Google OAuth
- Простая HTML‑страница в `templates`

**Структура проекта**
- `main.py` — точка входа FastAPI, подключение роутов и статики
- `handlers/` — HTTP‑роуты (auth, tasks, notes, user, ui, ping)
- `service/` — бизнес‑логика (auth, task, note, user)
- `repository/` — работа с БД
- `models/` — SQLAlchemy‑модели
- `schema/` — Pydantic‑схемы
- `alembic/` и `alembic.ini` — миграции
- `templates/` и `static/` — UI и статика
- `Dockerfile`, `docker-compose.yml` — контейнеризация

**Переменные окружения**
Смотрите шаблон `/.env.example`. Для запуска создайте `/.env` и заполните:
- `POSTGRES_PASSWORD`, `DB_PASSWORD`, `DB_USER`, `DB_NAME`, `DB_HOST`, `DB_PORT`
- `JWT_SECRET_KEY`
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REDIRECT_URL`, `GOOGLE_TOKEN_URL`

**Запуск в Docker**
```bash
docker compose up --build
```

Приложение будет доступно на `http://localhost:8000`, БД на `localhost:5556`.

**Запуск локально без Docker**
1. Подготовить БД Postgres.
2. Создать `/.env` по примеру `/.env.example`.
3. Применить миграции:
```bash
alembic upgrade head
```
4. Запустить сервер:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Основные эндпоинты**
- `GET /` — UI
- `POST /user` — регистрация
- `POST /auth/login` — логин
- `GET /auth/login/google` — вход через Google
- `GET /auth/google` — OAuth callback
- `GET /task/all` — список задач
- `POST /task` — создать задачу
- `GET /task/{task_id}` — получить задачу
- `PATCH /task/{task_id}` — изменить имя
- `PATCH /task/{task_id}/status` — статус/дата/избранное
- `DELETE /task/{task_id}` — удалить
- `GET /notes/{task_id}` — получить заметку
- `PUT /notes/{task_id}` — обновить заметку
- `GET /ping/app` — проверка приложения

**Хранение заметок**
Заметки сохраняются в директории, заданной `NOTES_DIR` (по умолчанию `notes`). Для Docker используется volume `notes_data`.
