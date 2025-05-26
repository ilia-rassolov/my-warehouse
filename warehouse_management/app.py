from flask import (Flask, redirect, render_template, request,
                   url_for, flash, get_flashed_messages)
import os
from dotenv import load_dotenv

from .db import ProductRepository, OrderRepository, OrderItemRepository, DBClient
from .validator import validate
from .pack_data import pack


app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DEBUG'] = os.getenv('DEBUG')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def home():
    messages = get_flashed_messages(with_categories=True)
    return render_template('home.html', messages=messages,)


@app.route('/products')
def products():
    db = DBClient(DATABASE_URL)
    conn = db.open_connection()
    repo_products = ProductRepository(conn)
    products = repo_products.get_all_products()
    db.close_connection()
    messages = get_flashed_messages(with_categories=True)
    return render_template('products/products.html', products=products, messages=messages,)

@app.route('/products/add', methods=["GET", "POST"])
def add_product():
    if request.method == "GET":
        return render_template('products/create_product.html')
    if request.method == "POST":
        product_data = request.form.to_dict()
        errors = validate(product_data)
        if errors:
            flash(f"{errors}", 'error')
            return render_template('products/create_product.html',
                                   product=product_data), 422
        name_product = product_data.get('name')
        db = DBClient(DATABASE_URL)
        conn = db.open_connection()
        repo_product = ProductRepository(conn)
        id_existing = repo_product.get_id_by_name(name_product)
        if id_existing:
            flash(f"Товар с названием {product_data['name']} уже существует", 'info')
        else:
            id = repo_product.save(product_data)
            product = repo_product.get_product_by_id(id)
            db.commit_db()
            flash(f"Товар {product['name']} успешно добавлен", 'success')
        db.close_connection()
        return redirect(url_for('products'), code=302)

@app.route('/products/<id>')
def product_show(id):
    db = DBClient(DATABASE_URL)
    conn = db.open_connection()
    repo_products = ProductRepository(conn)
    product = repo_products.get_product_by_id(id)
    db.close_connection()
    if product:
        messages = get_flashed_messages(with_categories=True)
        return render_template('products/details_product.html', id=id,
                               product=product, messages=messages,)
    flash(f"Товар с ID {id} не существует", 'info')
    return redirect(url_for('products'), code=302)

@app.route('/products/update/<id>', methods=["GET", "POST"])
def update_product(id):
    if request.method == "GET":
        db = DBClient(DATABASE_URL)
        conn = db.open_connection()
        repo_products = ProductRepository(conn)
        product = repo_products.get_product_by_id(id)
        db.close_connection()
        return render_template('products/update_product.html', product=product), 422
    if request.method == "POST":
        product_data = request.form.to_dict()
        errors = validate(product_data)
        if errors:
            flash(f"{errors}", 'error')
            return render_template('products/update_product.html', id=id,
                                   product=product_data), 422
        db = DBClient(DATABASE_URL)
        conn = db.open_connection()
        repo_product = ProductRepository(conn)
        repo_product.update(id, product_data)
        db.commit_db()
        product = repo_product.get_product_by_id(id)
        db.close_connection()
        flash(f"Данные товара {product['name']} успешно обновлены", 'success')
        return redirect(url_for('products'), code=302)

@app.route('/products/delete/<id>', methods=["GET", "POST"])
def delete_product(id):
    if request.method == "GET":
        db = DBClient(DATABASE_URL)
        conn = db.open_connection()
        repo_products = ProductRepository(conn)
        product = repo_products.get_product_by_id(id)
        db.close_connection()
        return render_template('products/delete_product.html', product=product)
    if request.method == "POST":
        db = DBClient(DATABASE_URL)
        conn = db.open_connection()
        repo_product = ProductRepository(conn)
        product = repo_product.get_product_by_id(id)
        repo_product.delete(id)
        db.commit_db()
        flash(f"Товара {product['name']} успешно удален", 'success')
        return redirect(url_for('products'), code=302)


@app.route('/search')
def search_form():
    id_product_data = request.args.get("id_product_data")
    id_order_data = request.args.get("id_order_data")
    if id_product_data:
        return redirect(url_for('product_show', id=id_product_data), code=302)
    elif id_order_data:
        return redirect(url_for('order_show', id=id_order_data), code=302)


@app.route('/orders')
def orders():
    db = DBClient(DATABASE_URL)
    conn = db.open_connection()
    repo_orders = OrderRepository(conn)
    orders = repo_orders.get_all_orders()
    db.close_connection()
    messages = get_flashed_messages(with_categories=True)
    return render_template('orders/orders.html', orders=orders, messages=messages,)

@app.route('/orders/<id>')
def order_show(id):
    db = DBClient(DATABASE_URL)
    conn = db.open_connection()
    repo_orders = OrderRepository(conn)
    order = repo_orders.get_order_by_id(id)
    if order:
        repo_order_item = OrderItemRepository(conn)
        order_items = repo_order_item.get_by_order_id(id)
        db.close_connection()
        messages = get_flashed_messages(with_categories=True)
        return render_template('orders/details_order.html',
                               order=order, messages=messages, order_items=order_items,)
    db.close_connection()
    flash(f"Заказ с ID {id} не существует", 'info')
    return redirect(url_for('orders'), code=302)

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@app.route('/orders/add', methods=["GET", "POST"])
def add_order():
    if request.method == "GET":
        return render_template('orders/create_order.html')
    if request.method == "POST":
        data_create = request.form.to_dict(flat=False)
        order_status = request.form.get("status")

        logger.debug(f"Received data: {data_create}")
        quantity = request.form.getlist('quantity_data')
        product_ids = request.form.getlist('product_ids_data')
        submit_order = request.form.getlist('submit_order')

        logger.debug(f"Quantity: {quantity}, Product IDs: {product_ids}, submit_order: {submit_order}")

        db = DBClient(DATABASE_URL)
        conn = db.open_connection()

        repo_order = OrderRepository(conn)
        repo_order_item = OrderItemRepository(conn)
        repo_product = ProductRepository(conn)

        order_id = repo_order.save(order_status)

        order_items_data = pack(data_create, order_id)
        for order_item_data in order_items_data:
            product_id = order_item_data['product_id']
            product = repo_product.get_product_by_id(product_id)
            if not product:
                db.close_connection()
                flash(f"Товар с ID {order_item_data['product_id']} не существует", 'error')
                return redirect(url_for('orders'), code=302)
            stock_free = product['stock']
            stock_need = order_item_data['quantity']
            new_stock = stock_free - stock_need
            if new_stock < 0:
                db.close_connection()
                flash(f"Количество товара {product['name']} недостаточно", 'error')
                return redirect(url_for('orders'), code=302)
            repo_product.update_stock(product_id, new_stock)
            repo_order_item.save(order_item_data)
        db.commit_db()
        flash(f"Заказ с ID {order_id} успешно создан", 'success')
        db.close_connection()
        return redirect(url_for('orders'), code=302)


@app.route('/orders/<id>/status', methods=["GET", "POST"])
def update_status(id):
    if request.method == "GET":
        db = DBClient(DATABASE_URL)
        conn = db.open_connection()
        repo_orders = OrderRepository(conn)
        order = repo_orders.get_order_by_id(id)
        db.close_connection()
        return render_template('orders/update_status.html', order=order), 422
    if request.method == "POST":
        status_data = request.form.get('status')
        db = DBClient(DATABASE_URL)
        conn = db.open_connection()
        repo_order = OrderRepository(conn)
        repo_order.update(id, status_data)
        db.commit_db()
        db.close_connection()
        flash(f"Статус заказа ID {id} успешно обновлен", 'success')
        return redirect(url_for('orders'), code=302)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html',), 500
