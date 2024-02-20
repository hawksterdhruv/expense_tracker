from flask import Flask
from flask_restful import Api

from api import ExpensesApi, ExpenseApi
from db import db
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

username = 'dhruv'
password = 'dhruv'
database_name = 'expenses_tracker'
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://{username}:{password}@localhost/{database_name}'

db.init_app(app)

with app.app_context():
    db.create_all()

api = Api(app)
api.add_resource(ExpensesApi, "/expenses")
api.add_resource(ExpenseApi, "/expense/<int:expense_id>")

if __name__ == "__main__":
    app.run(debug=True)
