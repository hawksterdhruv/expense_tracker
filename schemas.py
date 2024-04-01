from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import Item, Bill


class ItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_instance = True
        include_fk = True

class BillSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Bill
        load_instance = True
