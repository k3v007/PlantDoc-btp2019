from flask import render_template, Blueprint


APP = Blueprint("APP", __name__)


@APP.route('/')
@APP.route('/home')
def index():
    return render_template('index.html')
