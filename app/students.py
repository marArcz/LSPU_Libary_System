from sys import prefix
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.students_auth import login_required
from app.db import get_db

bp = Blueprint('students', __name__)


@bp.route("/")
def index():
    return render_template('students/home.html.jinja')