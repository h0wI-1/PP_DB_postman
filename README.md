# ПИ лаба 4 — тестирование БД через Postman

Учебный проект: интернет-магазин техники.
Стек: **PostgreSQL + PostgREST + Postman**.

## Структура репозитория

```
ПИ лаба 4/
├── sql/
│   ├── 01_schema.sql        DDL — 4 таблицы, FK, индексы
│   ├── 02_seed.sql          тестовые данные
│   └── 03_security.sql      роли web_anon/web_user, users, login()
├── config/
│   └── postgrest.conf       конфиг PostgREST (порт 3000)
├── postman/
│   ├── ShopAPI.postman_collection.json   коллекция запросов + автотесты
│   └── ShopAPI.postman_environment.json  environment (base_url, token, ...)
├── docs/
│   ├── report.md            готовый текст отчёта (9 разделов)
│   ├── screenshots.md       shot list (22 скриншота)
│   └── run_instructions.md  инструкция запуска
└── CLAUDE.md                контекст проекта
```

## Порядок действий

1. Поставить PostgreSQL, PostgREST, pgjwt, Postman.
2. Создать БД `shop_db`, прогнать скрипты `sql/01_*.sql` → `sql/02_*.sql` → `sql/03_*.sql`.
3. Запустить PostgREST: `postgrest config/postgrest.conf`.
4. Импортировать в Postman коллекцию и environment из `postman/`.
5. Запустить `POST /rpc/login` — токен сохранится автоматически.
6. Открыть Collection Runner и прогнать всю коллекцию.
7. Собрать скриншоты по `docs/screenshots.md`.
8. Сдать отчёт из `docs/report.md`.

Подробности — в `docs/run_instructions.md`.

## Тестовые учётные данные

- email: `admin@shop.local`
- пароль: `password123`

## Важное про формулировку PULL

В задании есть метод `PULL`, которого в HTTP не существует. Для PostgREST
применяется `PATCH` (частичное обновление). Это поясняется в разделе 5.3
отчёта.
