from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import DataRequired, Length


class LitterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired('Add meg az alom nevét!'),
                                           Length(message='150 karakter lehet az alom neve maxumim!', max=150)])

