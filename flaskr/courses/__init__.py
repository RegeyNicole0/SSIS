from flask import Blueprint

courses_view = Blueprint('courses_view', __name__)

from . import controller