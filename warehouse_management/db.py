import psycopg2
from psycopg2.extras import DictCursor
from psycopg2 import OperationalError, DatabaseError
import logging


class ProductRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_all_products(self):
        with self.conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute("""
                   SELECT
                       products.id AS product_id,
                       products.name AS product_name,
                       products.description AS product_description,
                       products.price AS product_price,
                       products.stock AS product_stock
                   FROM products
                   ORDER BY products.id;""")
            products = [dict(row) for row in curs]
        return products

    def get_product_by_id(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute("SELECT * FROM products WHERE id = %s", (id,))
            row = curs.fetchone()
        return dict(row) if row else dict()

    def save(self, new_product):
        placeholders = ', '.join(f'%({k})s' for k in new_product)
        query = (f"""INSERT INTO products
                          ({', '.join(new_product)}) VALUES ({placeholders})
                          RETURNING id""")
        with self.conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, new_product)
            id = curs.fetchone()['id']
        return id

    def update(self, product_id, product_data):
        placeholders = (
            product_data['name'],
            product_data['description'],
            product_data['price'],
            product_data['stock']
        )
        query = (
            f"""
            UPDATE products
            SET name = %s,
                description = %s,
                price = %s,
                stock = %s
            WHERE id = {product_id};"""
        )
        with self.conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, placeholders)
        return None

    def delete(self, product_id):
        with self.conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(f"""DELETE FROM products
                     WHERE id = {product_id};"""
                         )
        return None

    def get_id_by_name(self, name):
        with self.conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(f"""SELECT id FROM products
             WHERE name = %s;""", (name,))
            try:
                id = curs.fetchone()['id']
            except TypeError:
                id = None
        return id

    def update_stock(self, product_id, new_stock):
        query = (
            f"""
            UPDATE products
            SET stock = %s
            WHERE id = {product_id};"""
        )
        with self.conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, (new_stock,))
        return None


class OrderRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_all_orders(self):
        with self.conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute("""
                   SELECT
                       orders.id AS order_id,
                       orders.status AS order_status,
                       orders.created_at AS order_created_at
                   FROM orders
                   ORDER BY orders.id;""")
            orders = [dict(row) for row in curs]
        return orders

    def get_order_by_id(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute("SELECT * FROM orders WHERE id = %s", (id,))
            row = curs.fetchone()
        return dict(row) if row else None

    def save(self, order_status):
        query = (f"""INSERT INTO orders
                          (status) VALUES ('{order_status}')
                          RETURNING id""")
        with self.conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query)
            curs.execute(query, (order_status,))
            id = curs.fetchone()['id']
        return id

    def update(self, id, order_status):
        query = (
            f"""
            UPDATE orders
            SET status = '{order_status}'
            WHERE id = {id};"""
        )
        with self.conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query)
        return None

class OrderItemRepository:
    def __init__(self, conn):
        self.conn = conn

    def save(self, order_element):
        placeholders = ', '.join(f'%({k})s' for k in order_element)
        query = (f"""INSERT INTO order_item
                          ({', '.join(order_element)}) VALUES ({placeholders})
                          """)
        with self.conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute(query, order_element)
        return None

    def get_by_order_id(self, order_id):
        with self.conn.cursor(cursor_factory=DictCursor) as curs:
            curs.execute("SELECT * FROM order_item WHERE order_id = %s", (order_id,))
            order_items = [dict(row) for row in curs]
        return order_items


class DBClient:
    def __init__(self, db):
        self.db = db
        self.conn = None

    def open_connection(self):
        try:
            self.conn = psycopg2.connect(self.db)
        except (OperationalError, DatabaseError) as err:
            logging.error(err)
        return self.conn

    def commit_db(self):
        return self.conn.commit()

    def close_connection(self):
        return self.conn.close()
