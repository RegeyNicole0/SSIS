from . import courses_view

@courses_view.route('/courses', methods=['GET','POST'])
def index():
    return "<h1>Hello Courses! </h1>"