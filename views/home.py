from flask import render_template, Blueprint

home_page = Blueprint("home_page", __name__)


@home_page.route('/')
def home():
    return render_template('index.html')


@home_page.route('/bill')
def bill():
    return render_template('bill.html')
