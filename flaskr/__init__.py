from flask import Flask
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY']=SECRET_KEY
    app.config['MYSQL_HOST'] = DB_HOST
    app.config['MYSQL_USER'] = DB_USERNAME
    app.config['MYSQL_PASSWORD'] = DB_PASSWORD
    app.config['MYSQL_DATABASE'] = DB_NAME

    from .colleges import colleges_view
    from .courses import courses_view
    from .students import students_view
    
    app.register_blueprint(colleges_view, url_prefix='/')
    app.register_blueprint(courses_view, url_prefix='/')
    app.register_blueprint(students_view, url_prefix='/')
    
    return app