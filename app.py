from flask import Flask, render_template, flash, request, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import hashlib
import string
import redis


def hash_url(url, precision=10):
    alphabet = string.digits + string.ascii_letters
    base = len(alphabet)

    def num62(num):
        if num // base > 0:
            return num62(num // base) + alphabet[num % base]
        else:
            return alphabet[num]

    return num62(int(hashlib.md5(url.encode("UTF-8")).hexdigest(), 16) % (10 ** precision))


DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '623519030e6f'

redis_db = redis.StrictRedis(host="redis", port=6379, db=0)


class ReusableForm(Form):
    url = TextField('Page:', validators=[validators.required()])


@app.route('/', methods=['GET', 'POST'])
def home_page():
    page = ''
    form = ReusableForm(request.form)
    print(form.errors)

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
        return '<meta http-equiv="refresh" content="0; url=%s" />' % redis_db.get(url).decode("UTF-8")
        #return '<html><body><a href="%s">moved here</a></body></html>' % redis_db.get(url).decode("UTF-8")
    else:
        return redirect("/", code=302)


if __name__ == "__main__":
    app.run(host= '0.0.0.0')
