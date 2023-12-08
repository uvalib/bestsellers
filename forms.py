from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectMultipleField, HiddenField
from wtforms import FormField, widgets, FieldList, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

def password_validator(form, field):
    password = field.data
    if len(password) < 1:
        raise ValidationError('You must enter password')
    
