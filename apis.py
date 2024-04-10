import logging
import os
import pprint
from pathlib import Path

from PIL import Image
from flask import request, redirect, jsonify, url_for, current_app
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename, send_file
import pytesseract as pt

from db import db
from models import Item, Bill, UnprocessedBill
from schemas import ItemSchema, BillSchema, UnprocessedBillSchema

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
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
        return redirect(url_for('apis.itemapi', item_id=item_obj.id)), 201


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
        bill_raw = request.json
        logger.debug("Incoming data : %s", bill_raw)
        bill_obj = self.bill_schema.load(bill_raw, session=db.session)
        db.session.add(bill_obj)
        db.session.commit()
        logger.debug("Created new bill object %s", bill_obj)
        return redirect(url_for('apis.billapi', bill_id=bill_obj.id))


class UnprocessedBillsApi(Resource):
    unprocessed_bill_schema = UnprocessedBillSchema()

    def post(self):
        if (file := request.files.get('file')) is None:
            return 'No file part in the request.', 400

        if file.filename == '':
            return 'No selected file.', 400

        if file.filename.rsplit('.')[-1] not in ['jpg', 'png', 'jpeg']:
            return 'Incorrect file format. Please upload images files (jpg, png, jpeg)', 400

        # TODO : rename file
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        unprocessed_bill = UnprocessedBill()
        unprocessed_bill.raw_image = filename
        db.session.add(unprocessed_bill)
        db.session.commit()
        return jsonify({'unprocessed_bill.id': unprocessed_bill.id}), 201

    def get(self):
        temp = db.session.query(UnprocessedBill)
        return self.unprocessed_bill_schema.dump(temp, many=True)


class UnprocessedBillApi(Resource):
    unprocessed_bill_schema = UnprocessedBillSchema()

    def get(self, unprocessed_bill_id):
        temp = db.get_or_404(UnprocessedBill, unprocessed_bill_id)
        # logger.debug(temp[0].raw_image)
        return self.unprocessed_bill_schema.dump(temp)


class Process(Resource):
    def get(self, unprocessed_bill_id: int):
        unprocessed_bill = db.get_or_404(UnprocessedBill, unprocessed_bill_id)
        logger.info(pprint.pformat(unprocessed_bill.__dict__))
        filepath = Path(current_app.config['UPLOAD_FOLDER']) / unprocessed_bill.raw_image
        img = Image.open(filepath)
        data = pt.image_to_string(img, lang='eng')
        data = data.split('\n')
        return jsonify({"data": data})


class Resource(Resource):
    def get(self, unprocessed_bill_id):
        """
        CDN method for resource files.
        Add logic to disallow direct/outside/user access
        :param:
        :return:
        """
        temp = db.get_or_404(UnprocessedBill, unprocessed_bill_id)
        filepath = Path(current_app.config['UPLOAD_FOLDER']) / temp.raw_image
        return send_file(filepath, environ=request.environ)
