import functools
from webbrowser import get

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('admin_auth', __name__, url_prefix='/admin/auth')

@bp.before_app_request
def load_logged_in_user():
    account_id = session.get('admin_id')

    if account_id is None:
        g.admin = None
    else:
        g.admin = get_db().execute(
            'SELECT * FROM admin WHERE id = ?', (account_id,)
        ).fetchone()


# Route Signing up admin
@bp.route('/signup', methods=('GET','POST'))
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        
        error = None
        if error is None:
            try:
                db.execute(
                    'INSERT INTO admin(email,username,password) VALUES(?,?,?)',(email,username,generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f"Email {email} is already taken."
            else:
                flash('Successfully created an account, sign in to continue!')
                return redirect(url_for("admin_auth.signin"))
        flash(error)    
        
    else:
        db = get_db()
        admin = db.execute('SELECT COUNT(*) as count FROM admin').fetchone()

        if int(admin['count']) > 0:
            return redirect(url_for('admin_auth.signin'))

    return render_template('admin/auth/signup.html.jinja')


# Route for login
@bp.route('/signin',methods=('POST','GET'))
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()

        admin = db.execute(
            'SELECT * FROM admin WHERE username = ?',(username,)
        ).fetchone()
        
        error = None
        if admin is None:
            error = "Invalid sign in credentials!"
        elif not check_password_hash(admin['password'], password):
            error = "Incorrect Password!"

        if error is None:
            session['admin_id'] = admin['id']
            flash('Successfully signed in!')
            return redirect(url_for('admin.dashboard'))
        flash(error)
    else:
        db = get_db()
        admin = db.execute('SELECT COUNT(*) as count FROM admin').fetchone()

        if admin['count'] == 0:
            return redirect(url_for('admin_auth.signup'))

    return render_template('admin/auth/signin.html.jinja')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return redirect(url_for('admin_auth.signin'))

        return view(**kwargs)

    return wrapped_view