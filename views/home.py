import logging

from flask import render_template, Blueprint, current_app

home_page = Blueprint("home_page", __name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_navs():
    return [{'text': a.endpoint, 'href': a.rule} for a in current_app.url_map.iter_rules()]


@home_page.route('/')
def home():
    endpoints = get_navs()
    return render_template('index.html', navs=endpoints)


@home_page.route('/bill')
def bill():
    return render_template('bill.html', navs=get_navs())


@home_page.route('/unprocessed-bills')
def unprocessed_bills():
    return render_template('unprocessed_bills.html', navs=get_navs())
