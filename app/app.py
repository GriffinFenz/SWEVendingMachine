from flask import render_template, request, jsonify, Blueprint
from app.models.machines import Machines
from app.models.products import Products
from app.models.machine_stock import MachineStock

bp = Blueprint("app", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route('/machine', methods=['GET'])
def read_machine():
    id = request.args.get("id")
    Products.query.all()
    MachineStock.query.all()
    if id is None:
        return jsonify(None)
    return jsonify(None)


# Need to finish this


@bp.route('/all-machines', methods=['GET'])
def get_all_machines():
    return jsonify(Machines.query.all())


# @bp.route('/machine/create', methods=['POST'])
# def create_machine():
#     if request.method == 'POST':
#         content = request.get_json(silent=True)
#         if content is None:
#             return jsonify(None)
#         cur = mysql.connection.cursor()
#         try:
#             loc = content['location']
#             name = content['machine_name']
#         except KeyError:
#             return jsonify(None)
#         if check_machine_duplicates(name, loc):
#             return jsonify(None)
#         query_statement = f"INSERT INTO machines(location, machine_name) VALUES ('{loc}', '{name}')"
#         cur.execute(query_statement)
#         mysql.connection.commit()
#         cur.close()
#         # Maybe redirect
#         return jsonify(content)
#     return jsonify(None)
#
#
# @bp.route('/machine/delete', methods=['POST'])
# def delete_machine():
#     if request.method == 'POST':
#         content = request.get_json(silent=True)
#         if content is None:
#             return jsonify(None)
#         try:
#             machine_id = content['machine_id']
#         except KeyError:
#             return jsonify(None)
#         cur = mysql.connection.cursor()
#         query_statement = f"DELETE from machine_products WHERE machine_id = {machine_id}"
#         cur.execute(query_statement)  # Hoping for a better way to delete from both tables at once
#         query_statement = f"DELETE from machines WHERE machine_id = {machine_id}"
#         cur.execute(query_statement)
#         mysql.connection.commit()
#         cur.close()
#         # Maybe redirect
#     return jsonify(None)
#
#
# @bp.route('/machine/edit', methods=['POST'])
# def edit_machine():
#     content = request.get_json(silent=True)
#     if content is None:
#         return jsonify(None)
#     try:
#         machine_id = content['machine_id']
#         loc = content['location']
#         name = content['machine_name']
#     except KeyError:
#         return jsonify(None)
#     if check_machine_duplicates(name, loc):
#         return jsonify(None)
#     cur = mysql.connection.cursor()
#     query_statement = f"UPDATE machines SET machine_name = '{name}', location = '{loc}' WHERE machine_id = {machine_id}"
#     cur.execute(query_statement)
#     mysql.connection.commit()
#     cur.close()
#     return jsonify(content)
#
#
# @bp.route('/item/', methods=['GET'])
# def read_item():
#     id = request.args.get("id")
#     if id is None:
#         return jsonify(None)
#     cur = mysql.connection.cursor()
#     query_statement = f"SELECT * from items WHERE item_id = {id}"
#     result_value = cur.execute(query_statement)
#     if result_value > 0:
#         item = cur.fetchone()
#         if request.method == 'GET':
#             cur.close()
#             return jsonify(item)
#     return jsonify(None)
#
#
# @flask_app.route('/all-products/', methods=['GET'])
# def get_all_products():
#     return jsonify(Machines.query.all())
#
#
# @bp.route('/item/create', methods=['POST'])
# def create_item():
#     if request.method == 'POST':
#         content = request.get_json(silent=True)
#         if content is None:
#             return jsonify(None)
#         cur = mysql.connection.cursor()
#         try:
#             name = content['item_name']
#             price = int(content['price'])
#         except KeyError or ValueError:
#             return jsonify(None)
#         query_statement = f"INSERT INTO items(item_name, price) VALUES ('{name}', {price})"
#         cur.execute(query_statement)
#         mysql.connection.commit()
#         cur.close()
#         # Maybe redirect
#         return jsonify(content)
#     return jsonify(None)
#
#
# @app.route('/item/delete', methods=['POST'])
# def delete_item():
#     if request.method == 'POST':
#         content = request.get_json(silent=True)
#         if content is None:
#             return jsonify(None)
#         cur = mysql.connection.cursor()
#         try:
#             item_id = content['item_id']
#         except KeyError:
#             return jsonify(None)
#         query_statement = f"DELETE from machine_products WHERE item_id = {item_id}"
#         cur.execute(query_statement)  # Hoping for a better way to delete from both tables at once
#         query_statement = f"DELETE from items WHERE item_id = {item_id}"
#         cur.execute(query_statement)
#         mysql.connection.commit()
#         cur.close()
#         # Maybe redirect
#     return jsonify(None)
#
#
# @app.route('/item/edit', methods=['POST'])
# def edit_item():
#     content = request.get_json(silent=True)
#     if content is None:
#         return jsonify(None)
#     try:
#         item_id = content['id']
#         price = content['price']
#     except KeyError:
#         return jsonify(None)
#     cur = mysql.connection.cursor()
#     query_statement = f"UPDATE items SET price = '{price}' WHERE item_id = {item_id}"
#     cur.execute(query_statement)
#     mysql.connection.commit()
#     cur.close()
#     return jsonify(content)
#
#
# @app.route('/stock/add', methods=['POST'])
# def add_stock_in_machine():
#     content = request.get_json(silent=True)
#     if content is None:
#         return jsonify(None)
#     try:
#         machine_id = content['machine_id']
#         item_id = content['item_id']
#         amount = int(content['amount'])
#     except KeyError or ValueError:
#         return jsonify(None)
#     cur = mysql.connection.cursor()
#     query_machine = f"SELECT * FROM machines WHERE machine_id = '{machine_id}'"
#     query_item = f"SELECT * FROM items WHERE item_id = '{item_id}'"
#     machines = cur.execute(query_machine)
#     items = cur.execute(query_item)
#     if machines > 0 and items > 0:
#         query_stock = f"INSERT INTO machine_products(machine_id, item_id, quantity)" \
#                       f" VALUES ('{machine_id}', '{item_id}', {amount})"
#         cur.execute(query_stock)
#         mysql.connection.commit()
#         cur.close()
#         return jsonify(content)
#     cur.close()
#     return jsonify(None)
#
#
# @app.route('/stock/edit', methods=['POST'])
# def edit_machine_stock():
#     content = request.get_json(silent=True)
#     if content is None:
#         return jsonify(None)
#     try:
#         machine_id = content['machine_id']
#         item_id = content['item_id']
#         amount = int(content['amount'])
#     except KeyError or ValueError:
#         return jsonify(None)
#     cur = mysql.connection.cursor()
#     query_machine = f"SELECT * FROM machines WHERE machine_id = '{machine_id}'"
#     query_item = f"SELECT * FROM items WHERE item_id = '{item_id}'"
#     machines = cur.execute(query_machine)
#     items = cur.execute(query_item)
#     if machines > 0 and items > 0:
#         query_stock = f"UPDATE machine_products SET quantity = '{amount}'" \
#                       f"WHERE (machine_id, item_id) = ('{machine_id}', '{item_id}')"
#         cur.execute(query_stock)
#         mysql.connection.commit()
#         cur.close()
#         return jsonify(content)
#     cur.close()
#     return jsonify(None)
#
#
# # Returns true if machine already exists in the database
# def check_machine_duplicates(name, location) -> bool:
#     cur = mysql.connection.cursor()
#     query = f"SELECT * FROM machines WHERE (location, machine_name) = ('{location}', '{name}')"
#     result = cur.execute(query)
#     cur.close()
#     if result > 0:
#         return True
#     return False
