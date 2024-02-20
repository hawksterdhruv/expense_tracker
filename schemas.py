from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import ExpenseModel


class ExpenseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ExpenseModel
        load_instance = True
