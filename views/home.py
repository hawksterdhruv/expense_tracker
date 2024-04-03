import logging
from pathlib import Path

from flask import render_template, Blueprint, current_app, send_file

home_page = Blueprint("home_page", __name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_navs() -> list[dict[str, str]]:
    navs = []
    for a in current_app.url_map.iter_rules():
        if 'apis' not in a.endpoint:
            navs.append({'text': a.endpoint, 'href': a.rule})
    return navs


@home_page.route('/')
def home():
    endpoints = get_navs()
    return render_template('index.html', navs=endpoints)


@home_page.route('/bill/<string:fname>')
def bill(fname: str):
    return render_template('bill.html', navs=get_navs(), fname=fname)


@home_page.route('/unprocessed-bills')
def unprocessed_bills():
    return render_template('unprocessed_bills.html', navs=get_navs())


@home_page.route('/resources/<string:fname>')
def resources(fname: str):
    """
    CDN method for resource files.
    Add logic to disallow direct/outside/user access
    :param fname:
    :return:
    """
    filepath = Path(current_app.config['UPLOAD_FOLDER']) / fname
    return send_file(filepath)
