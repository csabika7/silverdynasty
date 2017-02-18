from flask import Blueprint

litter = Blueprint('litter', __name__)

from . import views
