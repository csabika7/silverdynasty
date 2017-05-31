from flask import render_template, send_from_directory, jsonify
from silverdynasty import app, db
from silverdynasty.models import News, Cat, Litter, Wish
from silverdynasty.forms import WishForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', latest_news=News.latest())


@app.route('/news')
def news():
    return render_template('news.html', news_items=News.news_feed())


@app.route('/cats')
def cats():
    return render_template('cats.html', cats=Cat.for_sale(False))


@app.route('/kittens')
def kittens():
    return render_template('kittens.html', kittens=Cat.for_sale(True), form=WishForm())


@app.route('/litters')
def litters():
    return render_template('litters.html', litters=Litter.query.all())


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route("/images/<path:name>")
def get_image(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name, as_attachment=True)


@app.route("/wish", methods=['POST'])
def wish():
    form = WishForm()
    if form.validate():
        new_wish = Wish(name=form.name.data, email=form.email.data, details=form.details.data)
        db.session.add(new_wish)
        db.session.commit()
        return jsonify([('info', 'Előjegyzés elmentve!')]), 200
    return jsonify([('error', error) for errors in form.errors.values() for error in errors]), 400


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
