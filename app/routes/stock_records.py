from flask import Blueprint, jsonify, request, Response

from app.models.stock_record import StockRecord

record_bp = Blueprint("stock_records", __name__)


@record_bp.route("/product/records", methods=["GET"])
def get_product_time_stamp_in_records() -> Response:
    product_id = request.args.get("product_id")

    records = StockRecord.product_time_stamp_in_records(product_id=product_id)

    if records:
        return jsonify(Records=records, STATUS_CODE=200)
    return jsonify(STATUS_CODE=400)


@record_bp.route("/machine/records", methods=["GET"])
def get_machine_time_stamp_in_records() -> Response:
    machine_id = request.args.get("machine_id")

    records = StockRecord.machine_time_stamp_in_records(machine_id=machine_id)

    if records:
        return jsonify(Records=records, STATUS_CODE=200)
    return jsonify(STATUS_CODE=400)
