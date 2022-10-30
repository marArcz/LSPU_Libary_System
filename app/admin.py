from flask import (
    Blueprint, flash, g, jsonify, make_response, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from app.admin_auth import login_required
from app.db import get_db

bp = Blueprint('admin', __name__,url_prefix="/admin")

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
@bp.route('/add-student', methods=('POST','GET'))
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
            db.execute('INSERT INTO students(firstname,middlename,lastname,gender,year_level,email,password,student_id) VALUES(?,?,?,?,?,?,?,?)',(firstname,middlename,lastname,gender,year_level,email,password,student_id))
            db.commit()
        except:
            flash("System error, please try again!",'error')
        else:
            session['success'] = "Successfully added!"
        
    return redirect(url_for('admin.students'))

# add student
@bp.route('/edit-student', methods=('POST','GET'))
@login_required
def edit_student():
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
            db.execute('INSERT INTO students(firstname,middlename,lastname,gender,year_level,email,password,student_id) VALUES(?,?,?,?,?,?,?,?)',(firstname,middlename,lastname,gender,year_level,email,password,student_id))
            db.commit()
        except:
            flash("System error, please try again!",'error')
        else:
            session['success'] = "Successfully added!"
        
    return redirect(url_for('admin.students'))

# get students / returns json
@bp.route('/get-student',methods=("POST","GET"))
def get_student():
    if(request.method == "GET"):
        return redirect(url_for('admin.students'))
    else:
        id = request.form['id']
        db = get_db()

        student = db.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()

        if student:
            student_obj = {
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

