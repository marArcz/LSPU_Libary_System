from sys import prefix
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from app.admin_auth import login_required
from app.db import get_db

bp = Blueprint('admin', __name__)

@bp.before_app_request
def loadAdmin():
    if session['admin_id'] is not None:
        adminId = session['admin_id']
        db = get_db()
        admin = db.execute("SELECT * FROM admin WHERE id = ?", (adminId,))
    else:
        admin = None
    
    g.admin = admin

@bp.route("/admin/dashboard")
@login_required
def dashboard():
    return render_template('admin/dashboard.html.jinja')