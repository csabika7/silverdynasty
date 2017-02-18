from . import litter
from .forms import LitterForm
from silverdynasty import db
from silverdynasty.models import Litter
from flask import flash, render_template, redirect, url_for, request, jsonify
from flask_login import login_required


@litter.route('/list', methods=['GET', 'POST'])
@login_required
def list_litters():
    form = LitterForm()
    if form.validate_on_submit():
        db.session.add(Litter(name=form.name.data))
        db.session.commit()
        flash("Alom feltöltve: {}!".format(form.name.data), category='info')
        return redirect(url_for('.list_litters'))
    return render_template('/admin/litter/list.html', litters=Litter.query.all(), add_form=form)


@litter.route('/edit/<int:litter_id>', methods=['POST'])
@login_required
def edit_litter(litter_id):
    litter_item = Litter.query.get_or_404(litter_id)
    form = LitterForm(obj=litter_item)
    new_name = request.form['value']
    form.name.data = new_name
    if form.validate():
        form.populate_obj(litter_item)
        db.session.commit()
        return jsonify(('info', 'Alom sikeresen szerkesztve: {0}'.format(new_name))), 200
    return '\n'.join(form.errors['name']), 400
