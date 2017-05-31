from . import news
from .forms import NewsForm
from silverdynasty import db
from silverdynasty.models import News
from flask import flash, render_template, redirect, url_for
from flask_login import login_required
from datetime import datetime
from silverdynasty.util import save_file_field


@news.route('/list')
@login_required
def list_news():
    return render_template('/admin/news/list.html', news=News.news_feed())


@news.route('/edit/<int:news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    news_item = News.query.get_or_404(news_id)
    form = NewsForm(obj=news_item)
    if not form.picture.has_file():
        form.picture.data = news_item.picture
    if form.validate_on_submit():
        news_item.last_edited = datetime.utcnow()
        form.populate_obj(news_item)
        if form.picture.has_file():
            news_item.picture = save_file_field(form.picture)
        db.session.commit()
        flash('A bejegyzés elmentve!', category='info')
        return redirect(url_for('.list_news'))
    return render_template('/admin/news/manage.html', form=form, title='Hír szerkesztése')


@news.route('/add', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        event = form.event_happened.data
        pic_path = save_file_field(form.picture)
        db.session.add(News(title=title, picture=pic_path, content=content, event_happened=event))
        db.session.commit()
        flash('Bejegyzés elküldve: "{}"'.format(title), category='info')
        return redirect(url_for('.add_news'))
    return render_template('/admin/news/manage.html', form=form, title='Új hír publikálása')
