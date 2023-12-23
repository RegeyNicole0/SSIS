from email import message
from flask_wtf import FlaskForm
from wtforms import StringField, validators, FileField, SelectField
from wtforms.validators import Length, DataRequired, Regexp
from flask_wtf.file import FileRequired, FileAllowed

class AddStudent(FlaskForm):
    id = StringField(
        'ID Number', 
        validators=[
            Length(
                min=9,max=9, 
                message='Must be exactly 9 characters. (e.g. "2020-1971")',
                ), 
            DataRequired(message='ID Number is required'), 
            Regexp(
                '\A([0-9]{4})-([0-9]{4})\Z', 
                message='Cannot Submit, Invalid format for ID Number "YYYY-NNNN". (e.g. "2020-1971")',
                )
            ], 
        render_kw={'placeholder':"e.g. '2020-1971'"},
        )

    first_name = StringField(
        'First Name',
        validators=[
            Length(min=1, max=50), 
            DataRequired(message='First name is Required'), 
            Regexp(
                '\A\w+( \w+)*\Z', 
                message='Cannot submit, contains invalid characters or leading/trailing spaces',
                ),
            ],
        )

    last_name = StringField(
        'Last Name', 
        validators=[
            validators.Length(min=1, max=50),
            validators.DataRequired(message='Last name is Required'), 
            validators.Regexp(
                '\A\w+( \w+)*\Z', 
                message='Cannot submit, contains invalid characters or leading/trailing spaces',
                ),
            ],
        )
    profile_pic = FileField(
        'Profile Picture', 
        validators=[
            FileAllowed(['jpg','png'], message='Can only upload .jpg or .png files')
            ]
        )
    year = SelectField('Year Level', choices=[1,2,3,4,5])
    gender = SelectField('Gender', choices = ['Male','Female'])
    course = SelectField('Course')    
    




