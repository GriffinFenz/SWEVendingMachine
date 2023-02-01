from flask import request, jsonify, Blueprint
from app.models.machine_stock import MachineStock

stock_bp = Blueprint("stock", __name__)


@stock_bp.route('/stock/add', methods=['POST'])
def add_stock_in_machine():
    content = request.get_json(silent=True)
    try:
        product_id = content['product_id']
        machine_id = content['machine_id']
        amount = int(content['amount'])
    except KeyError:
        return jsonify(success=False, message="Missing product_id/machine_id parameter")
    except ValueError:
        return jsonify(success=False, message="Amount entered is not a valid number")
    if MachineStock.add_product_to_machine(product_id, machine_id, amount):
        return jsonify(MachineStock.find_by_ids(product_id, machine_id))
    return jsonify(success=False,
                   message=f"The Product with id: {product_id} already exists in Machine with id: {machine_id}")


@stock_bp.route('/stock/edit', methods=['PUT'])
def edit_stock_in_machine():
    content = request.get_json(silent=True)
    try:
        product_id = content['product_id']
        machine_id = content['machine_id']
        amount = int(content['amount'])
    except KeyError:
        return jsonify(success=False, message="Missing product_id/machine_id parameter")
    except ValueError:
        return jsonify(success=False, message="Amount entered is not a valid number")
    if MachineStock.edit_stock(product_id, machine_id, amount):
        return jsonify(MachineStock.find_by_ids(product_id, machine_id))
    return jsonify(success=False, message="The stock does not not currently exists")
