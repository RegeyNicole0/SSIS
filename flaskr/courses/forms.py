from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, SelectField
from wtforms.validators import Length, DataRequired, Regexp

class AddCourse(FlaskForm):
    course_code = StringField(
        'Course Code',
        validators=[
            Length(min=1, max=20), 
            DataRequired(message='Course Code is required'), 
            Regexp(
                '\A\w+( \w+)*\Z', 
                message='Cannot submit, contains invalid characters or leading/trailing spaces',
                ),
            ],
        render_kw={'placeholder':"e.g. 'BSCS'"},
        )

    course_name = StringField(
        'Course Name',
        validators=[
            validators.Length(min=1, max=100), 
            validators.DataRequired(message='Course Name is required'),
            validators.Regexp(
                '\A\w+( \w+)*\Z', 
                message='Cannot submit, contains invalid characters or leading/trailing spaces',
                ),
            ],
        )
    college = SelectField('College Origin', [validators.DataRequired()])