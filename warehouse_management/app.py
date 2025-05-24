from flask import (Flask, redirect, render_template, request,
                   url_for, flash, get_flashed_messages)
import os
from dotenv import load_dotenv

from .db import ProductRepository, DBClient
from .validator import validate


app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DEBUG'] = os.getenv('DEBUG')
DATABASE = os.getenv('DATABASE')


@app.route('/')
def home():
    messages = get_flashed_messages(with_categories=True)
    return render_template('home.html', messages=messages,)


@app.route('/products')
def products():
    db = DBClient(DATABASE)
    conn = db.open_connection()
    repo_products = ProductRepository(conn)
    products = repo_products.get_list()
    db.close_connection()
    messages = get_flashed_messages(with_categories=True)
    return render_template('products.html', products=products, messages=messages,)

@app.route('/search')
def search_form():
    id_data = request.args.get("id_data")
    return redirect(url_for('product_show', id=id_data), code=302)

@app.route('/products/add', methods=["GET", "POST"])
def add_product():
    if request.method == "GET":
        return render_template('create_product.html')
    if request.method == "POST":
        product_data = request.form.to_dict()
        errors = validate(product_data)
        if errors:
            flash(f"{errors}", 'error')
            return render_template('create_product.html',
                                   product=product_data), 422
        name_product = product_data.get('name')
        db = DBClient(DATABASE)
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
    db = DBClient(DATABASE)
    conn = db.open_connection()
    repo_products = ProductRepository(conn)
    product = repo_products.get_product_by_id(id)
    db.close_connection()
    if product:
        messages = get_flashed_messages(with_categories=True)
        return render_template('show.html', id=id,
                               product=product, messages=messages,)
    flash(f"Товар с ID {id} не существует", 'info')
    return redirect(url_for('products'), code=302)

@app.route('/products/update/<id>', methods=["GET", "POST"])
def update_product(id):
    if request.method == "GET":
        db = DBClient(DATABASE)
        conn = db.open_connection()
        repo_products = ProductRepository(conn)
        product = repo_products.get_product_by_id(id)
        db.close_connection()
        render_template('update_product.html', product=product), 422
    if request.method == "POST":
        product_data = request.form.to_dict()
        errors = validate(product_data)
        if errors:
            flash(f"{errors}", 'error')
            return render_template('update_product.html', id=id,
                                   product=product_data), 422
        db = DBClient(DATABASE)
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
        db = DBClient(DATABASE)
        conn = db.open_connection()
        repo_products = ProductRepository(conn)
        product = repo_products.get_product_by_id(id)
        db.close_connection()
        return render_template('delete_product.html', product=product)
    if request.method == "POST":
        db = DBClient(DATABASE)
        conn = db.open_connection()
        repo_product = ProductRepository(conn)
        product = repo_product.get_product_by_id(id)
        repo_product.delete(id)
        db.commit_db()
        flash(f"Товара {product['name']} успешно удален", 'success')
        return redirect(url_for('products'), code=302)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html',), 500
