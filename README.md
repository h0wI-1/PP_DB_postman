# ПИ лаба 4

Учебный проект: интернет-магазин техники.
Стек: **PostgreSQL + PostgREST + Postman + Swagger + Frontend (Макет)**.

## Структура репозитория

```
PP_DB_POSTMAN/
├── config/
│   └── postgrest.conf                    конфиг PostgREST (порт 3000)
├── docs/
│   ├── index.html                        HTML страница со Swagger
│   └── swagger.yaml                      Swagger схема
├── postman/
│   ├── ShopAPI.postman_collection.json   коллекция запросов + автотесты
│   └── ShopAPI.postman_environment.json  environment (base_url, token, ...)
├── sql/
│   ├── 01_schema.sql                     DDL — 4 таблицы, FK, индексы
│   ├── 02_seed.sql                       тестовые данные
│   └── 03_security.sql                   роли web_anon/web_user, users, login()
├── frontend.html                         макет фронтенда приложения
└── README.md                             контекст проекта
```
