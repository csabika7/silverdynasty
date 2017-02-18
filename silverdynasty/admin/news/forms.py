from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length
from datetime import datetime


class NewsForm(FlaskForm):
    title = StringField(id='title', label='Cím', validators=[DataRequired("Add meg a cikk címét!")])
    content = TextAreaField(id='content', label='Tartalom',
                            validators=[DataRequired("Írd meg a cikk tartalmát!"),
                                        Length(message="A cikk tartalma maximum 500 karakteres lehet!", max=500)])
    event_happened = DateTimeField(id='event_happened', label='Esemény ideje', default=datetime.utcnow)
