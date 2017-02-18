from datetime import datetime
from silverdynasty import db
from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    last_edited = db.Column(db.DateTime, default=datetime.utcnow)
    event_happened = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def latest():
        return News.query.order_by(desc(News.event_happened)).first()

    @staticmethod
    def news_feed():
        return News.query.order_by(desc(News.event_happened)).all()

    def __repr__(self):
        return '<News id="%d", title="%s", content="%s", posted="%s", last edited="%s">' \
               % (self.id, str(self.title), str(self.content), str(self.posted), str(self.last_edited))


class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    picture = db.Column(db.String(120))
    color = db.Column(db.String(80))
    color_code = db.Column(db.String(7))
    birth = db.Column(db.Date)
    gender = db.Column(db.String(6))
    description = db.Column(db.Text(500))
    status = db.Column(db.String(11))
    litter_id = db.Column(db.Integer, db.ForeignKey('litter.id'))

    AVAILABLE = 'AVAILABLE'
    RESERVED = 'RESERVED'
    SOLD = 'SOLD'
    NOT_SALABLE = 'NOT_SALABLE'
    STATUSES = {AVAILABLE: 'Elvihető', RESERVED: 'Foglalt',
                SOLD: 'Eladva', NOT_SALABLE: 'Nem eladó'}

    MALE = 'male'
    FEMALE = 'female'
    GENDERS = {'male': 'kandúr', 'female': 'nőstény'}

    @property
    def status_name(self):
        return self.STATUSES[self.status]

    @property
    def gender_name(self):
        return self.GENDERS[self.gender]

    def is_available(self):
        return self.status == Cat.AVAILABLE

    def is_reserved(self):
        return self.status == Cat.RESERVED

    @staticmethod
    def for_sale(is_for_sale):
        if is_for_sale:
            return Cat.query.filter((Cat.status == Cat.AVAILABLE) | (Cat.status == Cat.RESERVED)).all()
        return Cat.query.filter(Cat.status == Cat.NOT_SALABLE).all()

    def __repr__(self):
        return '<News id="%d" name="%s", picture="%s", color="%s", color code="%s",' \
               ' birth="%s", gender="%s", description="%s">' \
               % (self.id, str(self.name), str(self.picture), str(self.color), str(self.color_code),
                  str(self.birth), str(self.gender), str(self.description))


class Litter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    cats = db.relationship('Cat', backref='litter', lazy='dynamic')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(80))
    lastName = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(150))

    @property
    def password(self):
        raise AttributeError('Password is a read only property!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return 'User < id="%d", first name="%s", last name="%s", email="%s">' % (self.id, str(self.firstName),
                                                                                 str(self.lastName), str(self.email))


class Wish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160))
    email = db.Column(db.String(160))
    details = db.Column(db.String(1000))
