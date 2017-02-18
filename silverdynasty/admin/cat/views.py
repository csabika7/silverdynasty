from . import cat
from silverdynasty import db, app
from silverdynasty.models import Cat
from silverdynasty.admin.cat.forms import CatForm
from flask import flash, render_template, redirect, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename
import os


@cat.route('/list')
@login_required
def list_cats():
    return render_template('/admin/cat/list.html', cats=Cat.query.all())


@cat.route('/edit/<int:cat_id>', methods=['GET', 'POST'])
@login_required
def edit_cat(cat_id):
    cat_item = Cat.query.get_or_404(cat_id)
    form = CatForm(obj=cat_item)
    if not form.picture.has_file():
        form.picture.data = cat_item.picture
    if form.validate_on_submit():
        form.populate_obj(cat_item)
        if form.picture.has_file():
            cat_item.picture = save_picture(form.picture)
        db.session.commit()
        flash('A bejegyzés elmentve!', category='info')
        return redirect(url_for('.list_cats'))
    else:
        form.picture.data = cat_item.picture
    return render_template('/admin/cat/manage.html', form=form, title='Macska adatainak szerkesztése')


@cat.route('/add', methods=['GET', 'POST'])
@login_required
def add_cat():
    form = CatForm()
    if form.validate_on_submit():
        name = form.name.data
        color = form.color.data
        color_code = form.color_code.data
        birth = form.birth.data
        picture = form.picture
        gender = form.gender.data
        litter = form.litter.data.id
        status = form.status.data
        description = form.description.data
        create_cat(name, color, color_code, birth, picture, gender, litter, status, description)
        flash('Cica feltöltve: "{}"!'.format(name), category='info')
        return redirect(url_for('.add_cat'))
    return render_template('/admin/cat/manage.html', form=form, title='Új macska felvétele')


def create_cat(name, color, color_code, birth, picture, gender, litter, status, description):
    picture_name = save_picture(picture)
    new_cat = Cat(name=name, color=color, color_code=color_code, picture=picture_name,
                  birth=birth, gender=gender, description=description, litter_id=litter, status=status)
    db.session.add(new_cat)
    db.session.commit()


def save_picture(field):
    picture_name = secure_filename(field.data.filename)
    field.data.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_name))
    return picture_name
