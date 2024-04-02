from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import Item, Bill, UnprocessedBill


class ItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_instance = True
        include_fk = True


class BillSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Bill
        load_instance = True


class UnprocessedBillSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UnprocessedBill
        load_instance = True
