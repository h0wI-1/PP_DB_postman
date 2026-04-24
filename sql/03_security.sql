-- =====================================================================
-- Безопасность БД и авторизация по JWT
-- Создаём:
--   * роль web_anon   — анонимный доступ, только SELECT
--   * роль web_user   — авторизованный доступ, полный CRUD
--   * таблицу users   — логины/пароли (пароль хранится как хеш bcrypt)
--   * функцию login() — проверяет пароль и возвращает JWT
-- =====================================================================

-- Расширения
CREATE EXTENSION IF NOT EXISTS pgcrypto;   -- для crypt() / gen_salt()
CREATE EXTENSION IF NOT EXISTS pgjwt;      -- для sign() / verify()
-- Если расширение pgjwt не установлено в системе, см. инструкцию запуска
-- (раздел "Установка pgjwt" в docs/run_instructions.md).

-- ---------------------------------------------------------------------
-- Роли
-- ---------------------------------------------------------------------
DROP ROLE IF EXISTS web_user;
DROP ROLE IF EXISTS web_anon;

CREATE ROLE web_anon NOLOGIN;
CREATE ROLE web_user NOLOGIN;

-- Права для web_anon: только чтение
GRANT USAGE ON SCHEMA public TO web_anon;
GRANT SELECT ON clients, items, order_status, orders TO web_anon;

-- Права для web_user: полный CRUD + работа с последовательностями
GRANT USAGE ON SCHEMA public TO web_user;
GRANT SELECT, INSERT, UPDATE, DELETE
    ON clients, items, order_status, orders TO web_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO web_user;

-- Чтобы PostgREST мог переключаться на web_user при авторизации по JWT:
GRANT web_anon TO CURRENT_USER;
GRANT web_user TO CURRENT_USER;

-- ---------------------------------------------------------------------
-- Таблица пользователей (для логина)
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    email     VARCHAR(120) PRIMARY KEY,
    pass_hash TEXT         NOT NULL,
    role      NAME         NOT NULL
);

-- Тестовый пользователь: admin@shop.local / password123
INSERT INTO users (email, pass_hash, role) VALUES
    ('admin@shop.local', crypt('password123', gen_salt('bf')), 'web_user');

-- ---------------------------------------------------------------------
-- Функция login(): возвращает JWT
-- Секрет должен совпадать с jwt-secret из postgrest.conf
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.login(email TEXT, password TEXT)
RETURNS TABLE(token TEXT) AS $$
DECLARE
    _role NAME;
BEGIN
    SELECT u.role INTO _role
    FROM users u
    WHERE u.email = login.email
      AND u.pass_hash = crypt(login.password, u.pass_hash);

    IF _role IS NULL THEN
        RAISE invalid_password USING message = 'Invalid email or password';
    END IF;

    RETURN QUERY SELECT sign(
        row_to_json(r)::json,
        current_setting('app.jwt_secret')
    )::text
    FROM (
        SELECT _role AS role,
               login.email AS email,
               extract(epoch FROM now())::integer + 60 * 60 AS exp  -- 1 час
    ) r;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Разрешаем анонимному пользователю вызывать login()
GRANT EXECUTE ON FUNCTION public.login(TEXT, TEXT) TO web_anon;

-- ---------------------------------------------------------------------
-- Передаём секрет внутрь сессии PostgreSQL.
-- Значение должно совпадать с jwt-secret в postgrest.conf.
-- Чтобы оно читалось в функции login(), PostgREST передаёт его сам
-- (параметр jwt-secret), но для ручного тестирования из psql можно
-- выставить через ALTER DATABASE.
-- ---------------------------------------------------------------------
ALTER DATABASE shop_db SET "app.jwt_secret" TO 'super_secret_key_change_me_please_32chars';
