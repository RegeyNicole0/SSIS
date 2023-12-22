from flask import Blueprint

students_view = Blueprint('students_view', __name__)

from . import controller