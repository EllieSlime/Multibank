# Multibank API+Front

REST API для управления пользователями с аутентификацией через JWT токены, построенное на FastAPI, SQLAlchemy, PostgreSQL и Redis.

## 🚀 Быстрый старт (локальное развертывание)

### Требования

Перед началом убедитесь, что у вас установлены:

- **Docker** (версия 20.10+) и **Docker Compose** (версия 2.0+)
- **Git** для клонирования репозитория

Проверить установку:
```bash
docker --version
docker compose version
git --version
```

### Шаг 1: Клонирование репозитория

```bash
git clone <url-репозитория>
cd backend-activity
```

### Шаг 2: Настройка переменных окружения

Создайте файл `.env` в директории `src/` и в корне репозитория:

```bash
cd src
touch .env
```

Заполните файл `.env` следующими переменными:

```env
# PostgreSQL конфигурация
PSQL_DB=your_database_name
PSQL_USERNAME=your_db_user
PSQL_PASSWORD=your_secure_password
PSQL_DSN=postgresql+asyncpg://your_db_user:your_secure_password@db:5432/your_database_name

# Redis конфигурация
REDIS_DSN=redis://redis:6379/0

# JWT Security конфигурация
SECURITY_JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
SECURITY_ALGORITHM=HS256
SECURITY_ACCESS_TOKEN_EXPIRE=3600
SECURITY_REFRESH_TOKEN_EXPIRE_DAYS=30
```

**Важно:**
- Замените значения на свои (особенно пароли и `SECURITY_JWT_SECRET_KEY`)
- В продакшене используйте сильные секретные ключи
- Для генерации `SECURITY_JWT_SECRET_KEY` можно использовать:
  ```bash
  openssl rand -hex 32
  ```

### Шаг 3: Запуск проекта через Docker Compose

Вернитесь в корневую директорию проекта и запустите:

```bash
cd ..
docker compose up -d --build
```

Эта команда:
- Соберет образы для всех сервисов
- Запустит PostgreSQL, Redis, FastAPI и Nginx
- Автоматически выполнит миграции базы данных
- Запустит все сервисы в фоновом режиме

### Шаг 4: Проверка работоспособности

После запуска проверьте статус контейнеров:

```bash
docker compose ps
```

Все сервисы должны быть в статусе `Up`. Затем проверьте доступность:

1. **Главная страница (через Nginx):**
   ```
   http://localhost:8080
   ```

2. **Health Check:**
   ```
   http://localhost:8080/health
   ```
   Должен вернуть: `{"status": "healthy"}`

3. **Документация API (Swagger):**
   ```
   http://localhost:8080/docs
   ```

4. **Альтернативная документация (ReDoc):**
   ```
   http://localhost:8080/redoc
   ```

### Шаг 5: Просмотр логов

Для просмотра логов всех сервисов:
```bash
docker compose logs -f
```

Для просмотра логов конкретного сервиса:
```bash
docker compose logs -f api      # Логи FastAPI
docker compose logs -f db       # Логи PostgreSQL
docker compose logs -f redis    # Логи Redis
docker compose logs -f nginx    # Логи Nginx
```

## 🛠 Управление проектом

### Остановка сервисов

```bash
docker compose down
```

Остановит все контейнеры, но **сохранит данные** в volumes.

### Полная остановка с удалением данных

```bash
docker compose down -v
```

⚠️ **Внимание:** Это удалит все данные из базы данных!

### Перезапуск сервисов

```bash
docker compose restart
```

### Пересборка после изменений в коде

```bash
docker compose up -d --build
```

## 📁 Структура проекта

```
backend-activity/
├── docker-compose.yml          # Конфигурация Docker Compose
├── Dockerfile                  # Docker образ для FastAPI
├── nginx/
│   └── default.conf            # Конфигурация Nginx reverse proxy
├── src/
│   ├── .env                    # Переменные окружения (создайте сами)
│   ├── main.py                 # Точка входа FastAPI приложения
│   ├── requirements.txt        # Python зависимости
│   ├── alembic.ini             # Конфигурация Alembic (миграции)
│   ├── app/                    # Основной код приложения
│   │   ├── api_routes/         # API эндпоинты
│   │   ├── core/               # Конфигурация, безопасность, логирование
│   │   ├── crud/               # CRUD операции
│   │   ├── db/                 # Настройки базы данных
│   │   ├── models/             # SQLAlchemy модели
│   │   ├── schemas/            # Pydantic схемы
│   │   └── service/            # Бизнес-логика
│   ├── migrations/             # Миграции Alembic
│   ├── frontend/               # Статический фронтенд
│   └── tests/                  # Тесты
└── README.md                   # Этот файл
```

## 🌐 Доступ к сервисам

После запуска сервисы доступны по следующим адресам:

| Сервис | URL | Описание |
|--------|-----|----------|
| **Nginx** | `http://localhost:8080` | Главный вход (reverse proxy) |
| **FastAPI** | `http://localhost:8080` | Через Nginx |
| **PostgreSQL** | `localhost:5433` | Прямой доступ (если нужен) |
| **Redis** | `localhost:6379` | Прямой доступ (если нужен) |
| **API Docs** | `http://localhost:8080/docs` | Swagger UI |
| **ReDoc** | `http://localhost:8080/redoc` | ReDoc документация |

## 🔌 API Endpoints

### Пользователи

* `POST /api/v1/users` — Регистрация нового пользователя
* `GET /api/v1/users` — Получить информацию о текущем пользователе (требует JWT токен)

### Refresh Tokens

* `POST /api/v1/refresh-tokens` — Обновить access токен используя refresh токен

### Другие

* `GET /` — Главная страница (frontend)
* `GET /health` — Health check endpoint
* `GET /docs` — Swagger документация
* `GET /redoc` — ReDoc документация

## 🧪 Разработка

### Работа с миграциями

Миграции выполняются автоматически при запуске через Docker Compose. Если нужно создать новую миграцию:

```bash
docker compose exec api alembic revision --autogenerate -m "описание изменений"
docker compose exec api alembic upgrade head
```

### Запуск тестов

```bash
docker compose exec api pytest
```

### Доступ к базе данных

```bash
# Подключение к PostgreSQL
docker compose exec db psql -U your_db_user -d your_database_name
```

### Доступ к Redis CLI

```bash
docker compose exec redis redis-cli
```

## 🔧 Решение проблем

### Порт уже занят

Если порт 8080 занят, измените в `docker-compose.yml`:
```yaml
nginx:
  ports:
    - "8081:80"  # Измените 8081 на свободный порт
```

### Ошибки подключения к базе данных

1. Убедитесь, что `.env` файл создан и правильно заполнен
2. Проверьте логи: `docker compose logs db`
3. Убедитесь, что база данных запустилась: `docker compose ps`

### Ошибки миграций

Если миграции не применились:
```bash
docker compose exec api alembic upgrade head
```

### Очистка и перезапуск

Если что-то пошло не так:
```bash
docker compose down -v
docker compose up -d --build
```

## 📝 Заметки

- FastAPI автоматически перезагружается при изменении кода благодаря volume mount `./src:/app`
- Все данные PostgreSQL сохраняются в Docker volume `postgres_data`
- Nginx работает как reverse proxy перед FastAPI
- Redis используется для rate limiting и кэширования

## 🚀 Продакшн

⚠️ **Важно:** Перед развертыванием в продакшн:

1. Измените все пароли и секретные ключи
2. Настройте правильные CORS origins
3. Используйте HTTPS
4. Настройте правильные логи и мониторинг
5. Убедитесь, что все зависимости обновлены

---

**Удачи в разработке! 🎉**
