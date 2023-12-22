from flask import Blueprint

colleges_view = Blueprint('colleges_view', __name__)

from . import controller