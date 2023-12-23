from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField
from wtforms.validators import Length, DataRequired, Regexp



class AddCollege(FlaskForm):
    college_code = StringField(
        'College Code',
        validators=[
            Length(min=1, max=20),
            DataRequired(message='College Code is required'),
            Regexp(
                '\A\w+( \w+)*\Z', 
                message='Cannot submit, contains invalid characters or leading/trailing spaces',
                ),
            ],
        render_kw={'placeholder':"e.g. 'CCS'"}
        )

    college_name = StringField(
        'College Name',
        validators=[
            Length(min=1, max=100),
            DataRequired(message='College Name is required'),
            Regexp(
                '\A\w+( \w+)*\Z',
                message='Cannot submit, contains invalid characters or leading/trailing spaces',
                ),
            ],
        )