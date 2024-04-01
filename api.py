import logging

from flask import request, redirect, jsonify
from flask_restful import Resource, Api

from db import db
from models import Item, Bill
from schemas import ItemSchema, BillSchema

logging.basicConfig(level=logging.DEBUG)

api = Api()


class ItemApi(Resource):
    item_schema = ItemSchema()

    def get(self, item_id: int):
        item = db.get_or_404(Item, item_id)
        return self.item_schema.dump(item)

    def delete(self, item_id: int):
        item = db.get_or_404(Item, item_id)
        db.session.delete(item)
        db.session.commit()
        return self.item_schema.dump(item)


class ItemsApi(Resource):
    item_schema = ItemSchema()

    def get(self):
        # This is a legacy method. God only knows why because the new method is
        # downright insane.
        # NEW : db.session.execute(db.select(itemModel)).all()
        # Why the F would you do this?  And not even return itemModel objects at the end of all that?
        temp = db.session.query(Item)
        return self.item_schema.dump(temp, many=True)

    def post(self):
        item_obj = self.item_schema.load(request.json, session=db.session)
        db.session.add(item_obj)
        db.session.commit()
        return redirect(api.url_for(resource=ItemApi, item_id=item_obj.id))


class BillApi(Resource):
    bill_schema = BillSchema()

    def get(self, bill_id: int):
        bill = db.get_or_404(Bill, bill_id)
        return self.bill_schema.dump(bill)

    def delete(self, bill_id: int):
        bill = db.get_or_404(Bill, bill_id)
        db.session.delete(bill)
        db.session.commit()
        return self.bill_schema.dump(bill)


class BillsApi(Resource):
    bill_schema = BillSchema()

    def get(self):
        # This is a legacy method. God only knows why because the new method is
        # downright insane.
        # NEW : db.session.execute(db.select(billModel)).all()
        # Why the F would you do this?  And not even return billModel objects at the end of all that?
        temp = db.session.query(Bill)
        return self.bill_schema.dump(temp, many=True)

    def post(self):
        bill_obj = self.bill_schema.load(request.json, session=db.session)
        db.session.add(bill_obj)
        db.session.commit()
        return redirect(api.url_for(resource=BillApi, bill_id=bill_obj.id))
