from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms.fields import StringField, TextAreaField, DateField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Regexp
from silverdynasty.models import Litter, Cat


class CatForm(FlaskForm):
    name = StringField(id='name', label='Név', validators=[DataRequired("Add meg a cica nevét!"),
                                                           Length(message="Max. 120 karakter lehet a cica neve!",
                                                                  max=120)])
    picture = FileField(id='picture', label='Kép', validators=[DataRequired(message="Tölts fel képet a cicáról!"),
                                                               FileAllowed(['jpg', 'png'],
                                                                           """Csak kép tölthető fel!
                                                                           Megengedett formátumok: .jpg, .png""")])
    color = StringField(id='color', label='Színezet', validators=[DataRequired(message="Add meg a cica színét!"),
                                                                  Length(message="Max. 80 karakter lehet a cica színe!",
                                                                         max=80)])
    color_code = StringField(id='color_code', label='Szín kód',
                             validators=[DataRequired(message='Add meg a cica színkódját! Példa: MCO nt 21'),
                                         Regexp(regex='[A-Z]{3}\s?[a-z]{1,2}\s?\d{0,2}',
                                                message='Helytelen színkód! Példa: MCO nt 21')])
    birth = DateField(id='date_of_birth', label='Születési dátum',
                      validators=[DataRequired(message='Add meg a születési dátumát! Példa: 2016-01-05')])
    gender = SelectField(id='gender', label='Neme', choices=Cat.GENDERS.items())
    description = TextAreaField(id='description', label='Rövid leírás',
                                validators=[DataRequired('Írj egy rövid leírást a cicáről!')])
    status = SelectField(id='status', label='Eladási állapot', choices=Cat.STATUSES.items())
    litter = QuerySelectField(id='litter', label='Alom',
                              query_factory=lambda: [Litter(name='Szülő')] + Litter.query.all(),
                              get_pk=lambda litter: litter.id, get_label=lambda litter: litter.name)
