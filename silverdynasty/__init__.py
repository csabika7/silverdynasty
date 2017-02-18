from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from flask_sslify import SSLify
from logging import DEBUG, INFO
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = b'T\xfdS\xd4\xfa\xf8\xc4\x98u\x11z8\x06\xe3\xe8\xd2\xadJe\xf5\xf4f,\xbb'
# app.logger.setLevel(DEBUG)
app.logger.setLevel(INFO)

# configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'silver.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://<username>:<password>@' \
#                                         'csabika7.mysql.pythonanywhere-services.com/csabika7$silver'
# app.config['SQLALCHEMY_POOL_RECYCLE'] = 240
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.mkdir(app.config['UPLOAD_FOLDER'])
db = SQLAlchemy(app)
import silverdynasty.models

db.create_all()
db.session.commit()

# Configure Authentication
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)
login_manager.login_view = 'admin.login'
login_manager.login_message = 'Jelentkezz be, hogy elérhesd ezt az oldalt!'

# Configure SSL forcing
# sslify = SSLify(app, permanent=True)


# Configure CSRF for ajax
csrf = CsrfProtect()
csrf.init_app(app)

# Configure Blueprints
from silverdynasty.admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')
from silverdynasty.admin.cat import cat as cat_blueprint
app.register_blueprint(cat_blueprint, url_prefix='/admin/cat')
from silverdynasty.admin.news import news as news_blueprint
app.register_blueprint(news_blueprint, url_prefix='/admin/news')
from silverdynasty.admin.litter import litter as litter_blueprint
app.register_blueprint(litter_blueprint, url_prefix='/admin/litter')
