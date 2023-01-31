from flask import request, jsonify, Blueprint
from app.models.machines import Machines

machine_bp = Blueprint("machines", __name__)


@machine_bp.route('/machine', methods=['GET'])
def get_machine():
    machine_id = request.args.get("id")
    machine = Machines.find_by_id(machine_id)
    return jsonify(machine)


@machine_bp.route('/all-machines', methods=['GET'])
def get_all_machines():
    return jsonify(Machines.query.all())


@machine_bp.route('/machine/create', methods=['POST'])
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


@machine_bp.route('/machine/delete', methods=['DELETE'])
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


@machine_bp.route('/machine/edit', methods=['PUT'])
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