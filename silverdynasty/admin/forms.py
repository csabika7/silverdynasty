from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    email = StringField('email', validators=[DataRequired('Add meg az email címed!')])
    password = PasswordField('password', validators=[DataRequired('Add meg a jelszavad!')])
    remember_me = BooleanField('remember_me')
    submit = SubmitField('login')
