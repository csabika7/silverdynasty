from silverdynasty import app
from werkzeug.utils import secure_filename
import os


def save_file_field(field):
    picture_name = secure_filename(field.data.filename)
    field.data.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_name))
    return picture_name
