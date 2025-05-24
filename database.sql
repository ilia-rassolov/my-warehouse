DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS orders CASCADE;


CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(127) NOT NULL,
    description VARCHAR(255),
    price INTEGER NOT NULL,
    stock INTEGER DEFAULT 0
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    status VARCHAR(127) NOT NULL,
    created_at DATE DEFAULT CURRENT_DATE
);

CREATE TABLE order_item (
    id SERIAL PRIMARY KEY,
    product_id INT,
    order_id INT,
    quantity DECIMAL(10,1) NOT NULL
);
