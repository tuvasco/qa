# QA API

## 🚀 Запуск проекта

### 1. Клонировать репозиторий

### 2. Запустить контейнеры
```bash
docker-compose up -d --build
```

### 3. Применитб миграции
```bash
docker-compose run --rm app alembic upgrade head
```

### 4. Проверить работу API
Откройте Swagger UI:
```
http://localhost:8000/docs
```

Пример проверки:
1. `POST /questions` → создать вопрос  
```json
{ "text": "How are you?" }
```
2. `GET /questions` → убедиться, что вопрос появился.

---

## 🔧 Работа с миграциямим

Создать новую миграцию:
```bash
docker-compose run --rm app alembic revision --autogenerate -m "add answers table"
```

Применить все миграции:
```bash
docker-compose run --rm app alembic upgrade head
```

Откатить последнюю:
```bash
docker-compose run --rm app alembic downgrade -1
```

---

## 🗂 Структура проекта

- `app/` — исходный код приложения  
- `alembic/` — файлы миграций 
- `alembic.ini` — конфиг Alembic  
- `docker-compose.yml` — сервисы (app + db)  
- `.env` — настройкит окружения  

---
