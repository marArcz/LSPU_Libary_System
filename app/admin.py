from sqlite3 import IntegrityError, InternalError
import sqlite3
from flask import (
    Blueprint, flash, g, jsonify, make_response, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.admin_auth import login_required
from app.db import get_db

bp = Blueprint('admin', __name__,url_prefix="/admin")

# flashes an error message
def flash_error_msg(msg=None):
    if msg is None:
        msg = "System error, please try again!"
    
    return flash(msg, 'error')


@bp.before_app_request
def loadAdmin():
    if 'admin_id' in session:
        adminId = session['admin_id']
        db = get_db()
        admin = db.execute("SELECT * FROM admin WHERE id = ?", (adminId,)).fetchone()
    else:
        admin = None
    
    g.admin = admin

# dashboard
@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template('admin/dashboard.html.jinja')

# students
@bp.route('/students')
@login_required
def students():
    db = get_db()
    students = db.execute("SELECT * FROM students").fetchall()
    return render_template('admin/students.html.jinja',students=students,len=len(students))


# add student
@bp.route('/students/add', methods=('POST','GET'))
@login_required
def add_student():
    if(request.method == 'POST'):
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        gender = request.form['gender']
        year_level = request.form['year_level']
        password = request.form['password']
        student_id = request.form['student_id']
        email = ""

        db = get_db()

        try:
            db.execute('INSERT INTO students(firstname,middlename,lastname,gender,year_level,email,password,student_id) VALUES(?,?,?,?,?,?,?,?)',(firstname,middlename,lastname,gender,year_level,email,generate_password_hash(password),student_id))
            db.commit()
        except sqlite3.IntegrityError:
            flash("Cannot have duplicate values for Student IDs!",'error')
        else:
            flash("Successfully added")
        
    return redirect(url_for('admin.students'))

# edit student
@bp.route('/students/edit', methods=('POST','GET'))
@login_required
def edit_student():
    if(request.method == 'POST'):
        firstname = request.form['firstname']
        middlename = request.form['middlename']
        lastname = request.form['lastname']
        gender = request.form['gender']
        year_level = request.form['year_level']
        student_id = request.form['student_id']
        id = request.form['id']
        db = get_db()

        try:
            db.execute('UPDATE students SET firstname=?,middlename=?,lastname=?,gender=?,year_level=?,student_id=? WHERE id=?',(firstname,middlename,lastname,gender,year_level,student_id,id))
            db.commit()
        except db.IntegrityError:
            flash("System error, please try again!",'error')
        else:
            flash("Successfully updated")
        
    return redirect(url_for('admin.students'))

# get students / returns json
@bp.route('/students/get',methods=("POST","GET"))
def get_student():
    if(request.method == "GET"):
        return redirect(url_for('admin.students'))
    else:
        id = request.form['id']
        db = get_db()

        student = db.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()

        if student:
            student_obj = {
                'id':student['id'],
                'firstname': student['firstname'],
                'middlename': student['middlename'],
                'lastname': student['lastname'],
                'gender': student['gender'],
                'year_level': student['year_level'],
                'email': student['email'],
                'student_id': student['student_id']
            }

            return jsonify(student_obj)
        else:
            return make_response(jsonify(message="Cannot find student"))

# delete category
@bp.route('/students/delete')
def delete_student():
    id = request.args.get('id',type=int)

    db = get_db()

    try:
        db.execute('DELETE FROM students WHERE id = ?',(id,))
        db.commit()
    except:
        flash_error_msg()
    else:
        session['success'] = "Successfully deleted!"
    return redirect(url_for('admin.students'))

# categories
@bp.route('/categories')
@login_required
def categories():
    db = get_db()
    categories = db.execute("SELECT * FROM categories").fetchall()

    return render_template('admin/categories.html.jinja',categories=categories,len=len(categories))

# add category
@bp.route('/categories/add',methods=('POST','GET'))
@login_required
def add_category():
    if(request.method == "POST"):
        name = request.form['name']
        db=get_db()

        try:
            db.execute('INSERT INTO categories(name) VALUES(?)',(name,))
            db.commit()
        except:
            flash('System error, please try again!','error')
        else:
            flash("Successfully added")

    return redirect(url_for('admin.categories'))

# edit category
@bp.route('/categories/edit',methods=('POST','GET'))
@login_required
def edit_category():
    if(request.method == "POST"):
        name = request.form['name']
        id = request.form['id']
        db=get_db()

        try:
            db.execute('UPDATE categories SET name = ? WHERE id = ?',(name,id))
            db.commit()
        except:
            flash_error_msg()
        else:
            flash("Successfully updated")

    return redirect(url_for('admin.categories'))


# get one category / returns json
@bp.route('/categories/get',methods=("POST","GET"))
def get_category():
    if(request.method == "GET"):
        return redirect(url_for('admin.categories'))
    else:
        id = request.form['id']
        db = get_db()

        category = db.execute("SELECT * FROM categories WHERE id = ?", (id,)).fetchone()

        if category:
            obj = {
                'id':category['id'],
                'name':category['name']
            }

            return jsonify(obj)
        else:
            return make_response(jsonify(message="Cannot find category"))

# delete category
@bp.route('/categories/delete')
def delete_category():
    id = request.args.get('id',type=int)

    db = get_db()

    try:
        db.execute('DELETE FROM categories WHERE id = ?',(id,))
        db.commit()
    except:
        flash_error_msg()
    else:
        flash("Successfully deleted")
    return redirect(url_for('admin.categories'))

# authors
@bp.route('/authors')
@login_required
def authors():
    db = get_db()
    authors = db.execute('SELECT * FROM authors').fetchall()

    return render_template('admin/authors.html.jinja',authors=authors,len=len(authors))

# get author
@bp.route('/authors/get',methods=('POST',))
def get_author():
    id = request.form['id']
    db = get_db()
    author = db.execute('SELECT * FROM authors WHERE id=?',(id,)).fetchone()

    if author:
        return jsonify({
            'id':author['id'],
            'name':author['name'],
        })
    else:
        return jsonify({
            'message':'Cannot find author'
        })

# get author
@bp.route('/authors/delete')
@login_required
def delete_author():
    id = request.args.get('id')
    try:
        db = get_db()
        db.execute('DELETE FROM authors WHERE id=?',(id,))
        db.commit()
    except:
        flash_error_msg()
    else:
        flash('Successfully deleted')

    return redirect(url_for('admin.authors'))
# add authors
@bp.route('/authors/add',methods=('POST',"GET"))
@login_required
def add_author():
    if request.method == "POST":
        name = request.form['name']
        db = get_db()
        try:
            db.execute('INSERT INTO authors(name) VALUES(?)',(name,))
            db.commit()
        except:
            flash_error_msg()
        else:
            flash("Successfully added")
    return redirect(url_for('admin.authors'))

# edit authors
@bp.route('/authors/edit',methods=('POST',"GET"))
@login_required
def edit_author():
    if request.method == "POST":
        name = request.form['name']
        id = request.form['id']
        db = get_db()
        try:
            db.execute('UPDATE authors SET name=? WHERE id=?',(name,id))
            db.commit()
        except:
            flash_error_msg()
        else:
            flash("Successfully updated")
    return redirect(url_for('admin.authors'))
    

# books
@bp.route('/books')
@login_required
def books():
    db = get_db()
    books = db.execute('SELECT books.id,books.copies,books.category_id,books.author_id,books.title,books.date_published,books.sypnosis, categories.name as category_name, authors.name as author_name FROM books INNER JOIN categories ON books.category_id = categories.id INNER JOIN authors ON books.author_id = authors.id').fetchall()
    authors = db.execute('SELECT * FROM authors').fetchall()
    categories = db.execute('SELECT * FROM categories').fetchall()
    all_books = []

    for book in books:
        borrowed = db.execute("SELECT COUNT(*) as count FROM rental_details INNER JOIN rentals ON rental_details.id = rentals.id WHERE rentals.status != 1 AND rentals.status != 3 AND rental_details.book_id = ?", (book['id'],)).fetchone()['count']
        new_book = {**book, 'available':book['copies'] - borrowed}
        all_books.append(new_book)

    return render_template('admin/books.html.jinja',books=all_books,len=len(books),categories=categories,authors=authors)
# books
@bp.route('/books/add',methods=('POST','GET'))
@login_required
def add_book():
    if(request.method == "POST"):
        title = request.form['title']
        category_id = request.form['category_id']
        author_id = request.form['author_id']
        date_published = request.form['date_published']
        copies = request.form['copies']
        sypnosis = request.form['sypnosis']

        db = get_db()

        try:
            db.execute("INSERT INTO books(title,category_id,author_id,date_published,sypnosis,copies) VALUES(?,?,?,?,?,?)" ,(title,category_id,author_id,date_published,sypnosis,copies))
            db.commit()
        except:
            flash_error_msg()
        else:
            flash("Successfully added!")
    return redirect(url_for('admin.books'))

@bp.route('/books/edit',methods=('POST',))
@login_required
def edit_book():
    if(request.method == "POST"):
        id = request.form['id']
        title = request.form['title']
        category_id = request.form['category_id']
        author_id = request.form['author_id']
        date_published = request.form['date_published']
        sypnosis = request.form['sypnosis']
        copies = request.form['copies']
        db = get_db()

        try:
            db.execute("UPDATE books SET title=?,category_id=?,author_id=?,date_published=?,sypnosis=?,copies=? WHERE id=?" ,(title,category_id,author_id,date_published,sypnosis,copies,id))
            db.commit()
        except:
            flash_error_msg()
        else:
            flash("Successfully updated!")
    return redirect(url_for('admin.books'))

@bp.route('/books/get',methods=('POST','GET'))
def get_book():
    if(request.method == "POST"):
        id = request.form['id']
        db = get_db()

        book = db.execute("SELECT books.copies, STRFTIME('%m-%d-%Y',books.date_published) as date, books.id,books.category_id,books.author_id,books.title,books.sypnosis, categories.name as category_name, authors.name as author_name FROM books INNER JOIN categories ON books.category_id = categories.id INNER JOIN authors ON books.author_id = authors.id WHERE books.id = ?",(id,)).fetchone()
        borrowed = db.execute("SELECT COUNT(*) as count FROM rental_details INNER JOIN rentals ON rental_details.id = rentals.id WHERE rentals.status != 1 AND rentals.status != 3 AND rental_details.book_id = ?", (id,)).fetchone()['count']

        return jsonify({
            'title':book['title'],
            'id':book['id'],
            'sypnosis':book['sypnosis'],
            'date_published':book['date'],
            'category_id':book['category_id'],
            'author_id':book['author_id'],
            'category_name':book['category_name'],
            'author_name':book['author_name'],
            'copies':book['copies'],
            'available':book['copies'] - borrowed
        })

    return redirect(url_for('admin.books'))

@bp.route('/books/delete')
def delete_book():
    id = request.args.get('id')

    if id:
        db = get_db()
        try:
            db.execute('DELETE FROM books WHERE id = ?',(id,))
            db.commit()
        except:
            flash_error_msg()
        else:
            flash("Successfully deleted!")
    else:
        flash("Cannot find book",'error')
    return redirect(url_for('admin.books'))


@bp.route('/rentals')
@login_required
def rentals():
    db = get_db()
    rentals = db.execute("SELECT students.*,rentals.rental_no,rentals.status, STRFTIME('%m-%d-%Y',rentals.date_rented) as date FROM rentals INNER JOIN students ON rentals.student_id = students.id").fetchall()
    return render_template("admin/rentals.html.jinja",rentals=rentals,len=len(rentals))

