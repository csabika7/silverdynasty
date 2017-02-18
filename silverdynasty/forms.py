from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp


class WishForm(FlaskForm):
    name = StringField(id='name', label='Név', validators=[DataRequired('Kérjük adja meg a nevét!'),
                                                           Length(message="Maximum 160 karakter a neve!", max=160)])
    email = StringField(id='email', label='Email',
                        validators=[DataRequired('Kérjük adja meg az email címét!'),
                                    Regexp(regex='(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                                           message='Érvénytelen E-mail cím!'),
                                    Length(message='Maximum 160 karakter lehet az email cím!', max=160)])
    details = TextAreaField(id='details', label='Milyen cicát szeretnél?',
                            validators=[Length(message="Maximum 500 karakter!", max=500)])
