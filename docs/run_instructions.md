# Инструкция по запуску проекта

## 1. Что нужно установить

| Инструмент | Назначение | Ссылка |
|---|---|---|
| PostgreSQL 14+ | СУБД | https://www.postgresql.org/download/ |
| PostgREST      | REST-обёртка над PostgreSQL | https://postgrest.org/en/stable/tutorials/tut0.html |
| pgjwt          | Расширение PostgreSQL для JWT | https://github.com/michelp/pgjwt |
| Postman        | Клиент для HTTP-запросов | https://www.postman.com/downloads/ |
| DBeaver (по желанию) | GUI для БД, нужен для скриншотов схемы | https://dbeaver.io/ |

## 2. Создание базы данных

В терминале (macOS/Linux — `psql`, Windows — «SQL Shell (psql)»):

```bash
# зайти в psql под суперпользователем
psql -U postgres

# внутри psql
CREATE DATABASE shop_db;
\q
```

## 3. Применение SQL-скриптов

```bash
cd "path/to/ПИ лаба 4"

psql -U postgres -d shop_db -f sql/01_schema.sql
psql -U postgres -d shop_db -f sql/02_seed.sql
psql -U postgres -d shop_db -f sql/03_security.sql
```

После выполнения третьего скрипта в базе появятся роли `web_anon`, `web_user`,
таблица `users` и функция `login()`.

## 4. Установка pgjwt

pgjwt не входит в стандартную поставку PostgreSQL, его нужно поставить отдельно.

**macOS (Homebrew):**
```bash
brew install pgxnclient
pgxn install pgjwt
```

**Linux (вариант «из исходников»):**
```bash
git clone https://github.com/michelp/pgjwt.git
cd pgjwt
sudo make install
```

**Windows:** проще всего воспользоваться готовым Docker-образом PostgreSQL с
предустановленным pgjwt, например `postgrest/postgrest-compose`, либо
установить вручную через StackBuilder.

После установки повторно выполнить `sql/03_security.sql`.

### Если pgjwt поставить не удалось
Можно обойтись без него: закомментировать строку `CREATE EXTENSION pgjwt` и
удалить функцию `login()`. Тогда JWT генерируется вручную на https://jwt.io
с payload `{"role":"web_user"}` и тем же секретом, что в `postgrest.conf`.
Полученный токен вставляется в Postman в поле `token`. В отчёте это
оформляется как «генерация тестового токена для демонстрации авторизации».

## 5. Запуск PostgREST

```bash
cd "path/to/ПИ лаба 4"
postgrest config/postgrest.conf
```

В терминале должно появиться:
```
Listening on port 3000
Attempting to connect to the database...
Connection successful
```

## 6. Первая проверка в браузере

Открыть в браузере:
```
http://localhost:3000/clients
http://localhost:3000/items
```
Должен вернуться JSON-массив с данными из БД.

## 7. Импорт коллекции и environment в Postman

1. В Postman: `File` → `Import` → выбрать `postman/ShopAPI.postman_collection.json`.
2. Ещё раз `Import` → `postman/ShopAPI.postman_environment.json`.
3. В правом верхнем углу выбрать environment **Shop API Local**.
4. Запустить первый запрос `GET /clients`.

## 8. Получение токена

1. Выполнить запрос `POST /rpc/login` с телом:
   ```json
   { "email": "admin@shop.local", "password": "password123" }
   ```
2. В ответе придёт `token`. Скрипт Tests автоматически положит его в
   переменную environment `token`.
3. Дальше все защищённые запросы используют `Authorization → Bearer Token` со
   значением `{{token}}`.

## 9. Прогон коллекции

`Runner` → выбрать коллекцию `Shop API` → `Run`. Все тесты должны быть зелёными.
