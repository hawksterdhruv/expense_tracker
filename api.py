import logging

from flask import Flask, request, redirect
from flask_restful import Api, Resource

from db import db
from models import ExpenseModel
from schemas import ExpenseSchema

app = Flask(__name__)
api = Api(app)
username = 'dhruv'
password = 'dhruv'
database_name = 'expenses_tracker'
app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://{username}:{password}@localhost/{database_name}'


db.init_app(app)

logging.basicConfig(level=logging.DEBUG)

# class Db:
#     def crete_connection(self):
#         USERNAME = 'dhruv'
#         PASSWORD = 'dhruv'
#         HOST = 'localhost'
#         PORT = 3306
#
#     def init_database(self):
#         pass

with app.app_context():
    db.create_all()


class ExpensesApi(Resource):
    expense_schema = ExpenseSchema()

    def post(self):
        expense_obj = self.expense_schema.load(request.json, session=db.session)
        logging.debug(expense_obj)
        db.session.add(expense_obj)
        db.session.commit()
        return redirect(api.url_for(ExpenseApi, expense_id=expense_obj.id))


class ExpenseApi(Resource):
    expense_schema = ExpenseSchema()

    def get(self, expense_id: int):
        expense = db.get_or_404(ExpenseModel, expense_id)
        return self.expense_schema.dump(expense)


api.add_resource(ExpensesApi, "/expenses")
api.add_resource(ExpenseApi, "/expense/<int:expense_id>")

if __name__ == "__main__":
    app.run(debug=True)
