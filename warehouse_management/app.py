from flask import (Flask, redirect, render_template, request,
                   url_for, flash, get_flashed_messages)
import os
from dotenv import load_dotenv

from .db import ProductRepository, CheckRepository, DBClient
from .validator import validate, get_name
from .page_data import get_page_data


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
    products = repo_products.get_list()
    db.close_connection()
    return render_template('products.html', products=products,)


# @app.post('/products')
# def add_product():
#     url_data = request.form.get("url")
#     errors = validate(url_data)
#     if errors:
#         flash(f"{errors}", 'error')
#         messages = get_flashed_messages(with_categories=True)
#         return render_template('home.html', messages=messages), 422
#     name_url = get_name(url_data)
#     db = DBClient(DATABASE_URL)
#     conn = db.open_connection()
#     repo_urls = ProductRepository(conn)
#     id_existing = repo_urls.get_id_by_name(name_url)
#     if id_existing:
#         id = id_existing
#         flash('Страница уже существует', 'repeat')
#     else:
#         id = repo_urls.save_url(name_url)
#         db.commit_db()
#         flash('Страница успешно добавлена', 'success')
#     url = repo_urls.get_url_by_id(id)
#     db.close_connection()
#     return redirect(url_for('url_show', url=url, id=id), code=302)
#
#
# @app.route('/urls/<id>')
# def url_show(id):
#     db = DBClient(DATABASE_URL)
#     conn = db.open_connection()
#     repo_urls = ProductRepository(conn)
#     url = repo_urls.get_url_by_id(id)
#
#     repo_checks = CheckRepository(conn)
#     checks = repo_checks.get_checks(id)
#     db.close_connection()
#     messages = get_flashed_messages(with_categories=True)
#     return render_template('show.html',
#                            url=url, checks=checks, messages=messages,)
#
#
# @app.post('/urls/<id>/checks')
# def add_check(id):
#     db = DBClient(DATABASE_URL)
#     conn = db.open_connection()
#     repo_urls = ProductRepository(conn)
#     url = repo_urls.get_url_by_id(id)
#     new_check = get_page_data(url)
#     if new_check is None:
#         flash('Произошла ошибка при проверке', 'error')
#         return redirect(url_for('url_show', id=id), code=302)
#     repo_checks = CheckRepository(conn)
#     repo_checks.save_check(new_check)
#     db.commit_db()
#     db.close_connection()
#     flash('Страница успешно проверена', 'success')
#     return redirect(url_for('url_show', id=id), code=302)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html',), 500
