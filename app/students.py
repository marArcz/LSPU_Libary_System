from string import whitespace
from sys import prefix
from unicodedata import category
from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from app.students_auth import login_required
from app.db import get_db

bp = Blueprint('students', __name__)


@bp.route("/")
def index():
    db = get_db()
    categories = db.execute('SELECT * FROM categories').fetchall()
    return render_template('students/home.html.jinja',categories=categories)


@bp.route("/search")
def search_books():
    db = get_db()

    search_query = request.args.get('search_query')
    category = request.args.get("category")

    if search_query is None:
        search_query=""
    books = None
    
    books_count = db.execute("SELECT COUNT(*) as count FROM books WHERE isAvailable = 1").fetchone()['count']
    categories = db.execute("SELECT * FROM categories").fetchall()
    selected_category = None

    if category is not None or category is not whitespace:
        selected_category = db.execute("SELECT * FROM categories WHERE name = ? ",(category,)).fetchone()
        
    if selected_category is not None and categories is not None:
        books = db.execute("SELECT STRFTIME('%m-%d-%Y',books.date_published) as date, books.id,books.category_id,books.author_id,books.title,books.sypnosis, categories.name as category_name, authors.name as author_name FROM books INNER JOIN categories ON books.category_id = categories.id INNER JOIN authors ON books.author_id = authors.id WHERE (books.title LIKE ? OR books.sypnosis LIKE ?) AND books.category_id = ?",(f"%{search_query}%",f"%{search_query}%",selected_category['id'])).fetchall()
    else:
        books = db.execute("SELECT STRFTIME('%m-%d-%Y',books.date_published) as date, books.id,books.category_id,books.author_id,books.title,books.sypnosis, categories.name as category_name, authors.name as author_name FROM books INNER JOIN categories ON books.category_id = categories.id INNER JOIN authors ON books.author_id = authors.id WHERE (books.title LIKE ? OR books.sypnosis LIKE ?) ",(f"%{search_query}%",f"%{search_query}%",)).fetchall()

    return render_template('students/search.html.jinja',books=books,search_query=search_query,result_count=len(books),books_count=books_count,categories=categories,selected_category=selected_category)

@bp.route('/borrow')
def borrow_book():
    db = get_db()

    id = request.args.get('id')

    if g.student is None:
        return redirect(url_for('student_auth.signin') + "?redirect=" + url_for('students.borrow_book')+f"id={id}")
    
    if id is None:
        return redirect(url_for('students.search_books'))
    else:
        return
        


@bp.route('/borrow/add',methods=('POST',))
def add_book():
    db = get_db()

    id = request.form('id')

    list = session['borrowed_books']

    if list is None:
        list = [id,]
    else:
        list.append(id)

    session['borrowed_books'] = list

    return jsonify({'msg':'Successfully added'})

@bp.route('/borrow/get',methods=('POST',))
def get_selected_books():
    db = get_db()

    list = session.get('borrowed_books') #string : '1,2,3,4'

    if list is not None and len(list) > 0:
        books = db.execute("SELECT books.title, STRFTIME('%m-%d-%Y',books.date_published) as date, categories.name as category_name FROM books INNER JOIN categories WHERE id IN (?)",(len,)).fetchall()

        return jsonify({
            'books':books
        })
    else:
        return jsonify({
            'books':[]
        })

    