from flask import render_template, request, jsonify, Blueprint
from app.models.machines import Machines
from app.models.products import Products
from app.models.machine_stock import MachineStock

bp = Blueprint("app", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route('/machine', methods=['GET'])
def get_machine():
    machine_id = request.args.get("id")
    machine = Machines.find_by_id(machine_id)
    return jsonify(machine)


@bp.route('/all-machines', methods=['GET'])
def get_all_machines():
    return jsonify(Machines.query.all())


@bp.route('/machine/create', methods=['POST'])
def create_machine():
    content = request.get_json(silent=True)
    try:
        location = content['location']
        machine_name = content['machine_name']
    except KeyError:
        return jsonify(success=False, message="Missing location or/and machine_name parameters")
    # If machine exist then return machine else False run saying Machine exists
    if Machines.add_machine(machine_name, location):
        return jsonify(Machines.find_by_name(machine_name))
    return jsonify(success=False, message="Machine already exists")


@bp.route('/machine/delete', methods=['DELETE'])
def delete_machine():
    content = request.get_json(silent=True)
    try:
        machine_id = content['machine_id']
    except KeyError:
        return jsonify(success=False, message="Missing machine_id parameter")
    # If machine was deleted then show success message
    if Machines.remove_machine(machine_id):
        return jsonify(success=True, message=f"Machine with id: '{machine_id}' has been deleted")
    return jsonify(success=False, message=f"No machines that matches the id: '{machine_id}'")


@bp.route('/machine/edit', methods=['PUT'])
def edit_machine():
    content = request.get_json(silent=True)
    try:
        machine_id = content['machine_id']
        machine_name = content['machine_name']
        location = content['location']
    except KeyError:
        return jsonify(success=False, message="Missing machine_id/location/machine_name parameter")
    output_check = Machines.edit_machine(machine_id, machine_name, location)
    if output_check == 2:
        return jsonify(success=False, message=f"Machine with name: '{machine_name}' already belongs in the database")
    if output_check == 1:
        return jsonify(success=False, message=f"Machine with id: '{machine_id}' does not exist")
    return jsonify(Machines.find_by_id(machine_id))


@bp.route('/product/', methods=['GET'])
def get_product():
    product_id = request.args.get("id")
    product = Products.find_by_id(product_id)
    return jsonify(product)


@bp.route('/all-products/', methods=['GET'])
def get_all_products():
    return jsonify(Products.query.all())


@bp.route('/product/create', methods=['POST'])
def create_product():
    content = request.get_json(silent=True)
    try:
        price = int(content['price'])
        product_name = content['product_name']
    except KeyError:
        return jsonify(success=False, message="Missing price or/and product_name parameters")
    except ValueError:
        return jsonify(success=False, message="Price entered is not a valid number")
    # If product exist then return product else False run saying Product exists
    if Products.add_product(product_name, price):
        return jsonify(Products.find_by_name(product_name))
    return jsonify(success=False, message="Product already exists")


@bp.route('/product/delete', methods=['DELETE'])
def delete_product():
    content = request.get_json(silent=True)
    try:
        product_id = content['product_id']
    except KeyError:
        return jsonify(success=False, message="Missing product_id parameter")
    # If product was deleted then show success message
    if Products.remove_product(product_id):
        return jsonify(success=True, message=f"Product with id: '{product_id}' has been deleted")
    return jsonify(success=False, message=f"No products that matches the id: '{product_id}'")


@bp.route('/product/edit', methods=['PUT'])
def edit_product():
    content = request.get_json(silent=True)
    try:
        product_id = content['product_id']
        product_name = content['product_name']
        price = int(content['price'])
    except KeyError:
        return jsonify(success=False, message="Missing product_id/price/product_name parameter")
    except ValueError:
        return jsonify(success=False, message="Price entered is not a valid number")
    output_check = Products.edit_product(product_id, product_name, price)
    if output_check == 2:
        return jsonify(success=False, message=f"Product with name: '{product_name}' already belongs in the database")
    if output_check == 1:
        return jsonify(success=False, message=f"Product with id: '{product_id}' does not exist")
    return jsonify(Products.find_by_id(product_id))


@bp.route('/stock/add', methods=['POST'])
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


@bp.route('/stock/edit', methods=['PUT'])
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
