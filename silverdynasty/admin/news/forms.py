from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms.fields import StringField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length
from datetime import datetime


class NewsForm(FlaskForm):
    title = StringField(id='title', label='Cím', validators=[DataRequired("Add meg a cikk címét!")])
    content = TextAreaField(id='content', label='Tartalom',
                            validators=[DataRequired("Írd meg a cikk tartalmát!"),
                                        Length(message="A cikk tartalma maximum 1000 karakteres lehet!", max=1000)])
    picture = FileField(id='picture', label='Kép', validators=[DataRequired(message="Tölts fel képet a cikkről!"),
                                                               FileAllowed(['jpg', 'png'],
                                                                           """Csak kép tölthető fel!
                                                                           Megengedett formátumok: .jpg, .png""")])
    event_happened = DateTimeField(id='event_happened', label='Esemény ideje', default=datetime.utcnow)
