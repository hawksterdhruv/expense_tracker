from flask import Flask, Blueprint
from flask_restful import Api

from api import ItemsApi, ItemApi, BillApi, BillsApi
from db import db
import logging

from views.home import home_page

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

username = 'dhruv'
password = 'dhruv'
database_name = 'expenses_tracker'
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://{username}:{password}@localhost/{database_name}'

db.init_app(app)

with app.app_context():
    db.create_all()

api_bp = Blueprint('apis', __name__)

api = Api(api_bp)
api.add_resource(ItemsApi, "/items")
api.add_resource(ItemApi, "/item/<int:item_id>")
api.add_resource(BillsApi, "/bills")
api.add_resource(BillApi, "/bill/<int:bill_id>")

app.register_blueprint(api_bp, url_prefix='/api/v1')
app.register_blueprint(home_page, url_prefix='/')

if __name__ == "__main__":
    app.run(debug=True)
