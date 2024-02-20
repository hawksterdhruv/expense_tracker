import logging

from flask import request, redirect, jsonify
from flask_restful import Resource, Api

from db import db
from models import ExpenseModel
from schemas import ExpenseSchema

logging.basicConfig(level=logging.DEBUG)

api = Api()


class ExpenseApi(Resource):
    expense_schema = ExpenseSchema()

    def get(self, expense_id: int):
        expense = db.get_or_404(ExpenseModel, expense_id)
        return self.expense_schema.dump(expense)

    def delete(self, expense_id: int):
        expense = db.get_or_404(ExpenseModel, expense_id)
        db.session.delete(expense)
        db.session.commit()
        return self.expense_schema.dump(expense)


class ExpensesApi(Resource):
    expense_schema = ExpenseSchema()

    def get(self):
        # This is a legacy method. God only knows why because the new method is
        # downright insane.
        # NEW : db.session.execute(db.select(ExpenseModel)).all()
        # Why the F would you do this?  And not even return ExpenseModel objects at the end of all that?
        temp = db.session.query(ExpenseModel)
        return self.expense_schema.dump(temp, many=True)

    def post(self):
        expense_obj = self.expense_schema.load(request.json, session=db.session)
        db.session.add(expense_obj)
        db.session.commit()
        return redirect(api.url_for(resource=ExpenseApi, expense_id=expense_obj.id))
