from flask import render_template, Blueprint


APP = Blueprint("APP", __name__)


@APP.route('/', methods=['GET', ])
def index():
    render_template('index.html')
