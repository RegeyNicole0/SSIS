from . import students_view

@students_view.route('/students', methods=['GET','POST'])
def index():
    return "<h1>Hello Students! </h1>"