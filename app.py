from flask import Flask, render_template, flash, request, redirect
from wtforms import Form, validators
from wtforms.fields.html5 import URLField
import redis
from hash import hash_url


DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '623519030e6f'

redis_db = redis.StrictRedis(host="redis", port=6379, db=0)


class ReusableForm(Form):
    url = URLField('Page:', validators=[validators.required()])


@app.route('/', methods=['GET', 'POST'])
def home_page():
    page = ''
    form = ReusableForm(request.form)

    if request.method == 'POST':
        page = request.form['url']
        if form.validate():
            h = hash_url(page)
            redis_db.set(h, page)
            flash('Short link: ' + request.url + h)
        else:
            flash('Paste a link to shorten it. ')

    return render_template('index.html', form=form)


@app.route('/<url>')
def redirect_page(url):
    if redis_db.get(url):
        return redirect(redis_db.get(url).decode("UTF-8"), code=302)
    else:
        flash('A link not found.')
        return redirect("/", code=302)


if __name__ == "__main__":
    app.run(host= '0.0.0.0')
