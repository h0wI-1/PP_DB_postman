-- =====================================================================
-- Лабораторная работа 4
-- База данных: интернет-магазин техники
-- СУБД: PostgreSQL 14+
-- Схема: public
-- =====================================================================

-- Чистая пересборка схемы, чтобы скрипт можно было запускать повторно
DROP TABLE IF EXISTS orders         CASCADE;
DROP TABLE IF EXISTS order_status   CASCADE;
DROP TABLE IF EXISTS items          CASCADE;
DROP TABLE IF EXISTS clients        CASCADE;

-- ---------------------------------------------------------------------
-- Клиенты магазина
-- ---------------------------------------------------------------------
CREATE TABLE clients (
    id             SERIAL PRIMARY KEY,
    name           VARCHAR(100) NOT NULL,
    email          VARCHAR(120) NOT NULL UNIQUE,
    phone          VARCHAR(20),
    city           VARCHAR(80),
    registered_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ---------------------------------------------------------------------
-- Товары
-- ---------------------------------------------------------------------
CREATE TABLE items (
    id        SERIAL PRIMARY KEY,
    name      VARCHAR(120)   NOT NULL,
    category  VARCHAR(60)    NOT NULL,
    price     NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock     INTEGER        NOT NULL DEFAULT 0 CHECK (stock >= 0)
);

-- ---------------------------------------------------------------------
-- Справочник статусов заказа
-- ---------------------------------------------------------------------
CREATE TABLE order_status (
    id     SERIAL PRIMARY KEY,
    code   VARCHAR(20)  NOT NULL UNIQUE,
    title  VARCHAR(60)  NOT NULL
);

-- ---------------------------------------------------------------------
-- Заказы
-- ---------------------------------------------------------------------
CREATE TABLE orders (
    id          SERIAL PRIMARY KEY,
    client_id   INTEGER      NOT NULL REFERENCES clients(id)      ON DELETE CASCADE,
    item_id     INTEGER      NOT NULL REFERENCES items(id)        ON DELETE RESTRICT,
    status_id   INTEGER      NOT NULL REFERENCES order_status(id) ON DELETE RESTRICT,
    quantity    INTEGER      NOT NULL DEFAULT 1 CHECK (quantity > 0),
    total       NUMERIC(12, 2) NOT NULL CHECK (total >= 0),
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Индексы для ускорения выборок, которые будем делать через Postman
CREATE INDEX idx_items_price     ON items(price);
CREATE INDEX idx_clients_name    ON clients(name);
CREATE INDEX idx_orders_client   ON orders(client_id);
CREATE INDEX idx_orders_item     ON orders(item_id);
CREATE INDEX idx_orders_status   ON orders(status_id);
