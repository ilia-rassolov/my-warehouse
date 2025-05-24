import psycopg2
from psycopg2.extras import DictCursor
from psycopg2 import OperationalError, DatabaseError
import logging


class ProductRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_list(self):
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
        return dict(row) if row else None

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
