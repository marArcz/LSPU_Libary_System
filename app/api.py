from distutils.log import error
import functools

from flask import (
    Blueprint, flash, g, jsonify, make_response, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/books', methods=('POST',))
def get_books():
    if(request.method == "POST"):
        id = request.form['id']
        db = get_db()

        book = db.execute("SELECT STRFTIME('%m-%d-%Y',books.date_published) as date, books.id,books.category_id,books.author_id,books.title,books.sypnosis, categories.name as category_name, authors.name as author_name FROM books INNER JOIN categories ON books.category_id = categories.id INNER JOIN authors ON books.author_id = authors.id WHERE books.id = ?",(id,)).fetchone()

        return make_response(
            jsonify({
            'title':book['title'],
            'id':book['id'],
            'sypnosis':book['sypnosis'],
            'date_published':book['date'],
            'category_id':book['category_id'],
            'author_id':book['author_id'],
            'category_name':book['category_name'],
            'author_name':book['author_name'],
        })
        )