from flask import Flask, render_template, request, redirect, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.config['SECRET_KEY'] = "Never push this line to github public repo"

cred = yaml.load(open('cred.yaml'), Loader=yaml.Loader)
app.config['MYSQL_HOST'] = cred['mysql_host']
app.config['MYSQL_USER'] = cred['mysql_user']
app.config['MYSQL_PASSWORD'] = cred['mysql_password']
app.config['MYSQL_DB'] = cred['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/machine', methods=['GET'])
def read_machine():
    id = request.args.get("id")
    if id is None:
        return jsonify(None)
    cur = mysql.connection.cursor()
    query_statement = f"SELECT * from machines WHERE machine_id = {id}"
    query_statement_2 = f"SELECT * from machine_products WHERE machine_id = {id}"
    machines = cur.execute(query_statement)
    if machines > 0:
        machine = cur.fetchone()
        products = cur.execute(query_statement_2)
        if products > 0:
            product = cur.fetchall()
            cur.close()
            return jsonify(machine, product)
        else:
            cur.close()
            return jsonify(machine)
    return jsonify(None)


@app.route('/all-machines', methods=['GET'])
def read_all_machines():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        query_statement = f"SELECT * from machines"
        result = cur.execute(query_statement)
        if result > 0:
            machines = cur.fetchall()
            cur.close()
            return jsonify(machines)
    return jsonify(None)


@app.route('/machine/create', methods=['POST'])
def create_machine():
    if request.method == 'POST':
        content = request.get_json(silent=True)
        if content is None:
            return jsonify(None)
        cur = mysql.connection.cursor()
        try:
            loc = content['location']
            name = content['machine_name']
        except KeyError:
            return jsonify(None)
        query_statement = f"INSERT INTO machines(location, machine_name) VALUES ('{loc}', '{name}')"
        cur.execute(query_statement)
        mysql.connection.commit()
        cur.close()
        # Maybe redirect
        return jsonify(content)
    return jsonify(None)


@app.route('/machine/delete', methods=['POST'])
def delete_machine():
    if request.method == 'POST':
        content = request.get_json(silent=True)
        if content is None:
            return jsonify(None)
        cur = mysql.connection.cursor()
        try:
            machine_id = content['id']
        except KeyError:
            return jsonify(None)
        query_statement = f"DELETE from machine_products WHERE machine_id = {machine_id}"
        cur.execute(query_statement)  # Hoping for a better way to delete from both tables at once
        query_statement = f"DELETE from machines WHERE machine_id = {machine_id}"
        cur.execute(query_statement)
        mysql.connection.commit()
        cur.close()
        # Maybe redirect
    return jsonify(None)


@app.route('/machine/edit', methods=['POST'])
def edit_machine():
    content = request.get_json(silent=True)
    if content is None:
        return jsonify(None)
    try:
        machine_id = content['id']
        name = content['machine_name']
        loc = content['location']
    except KeyError:
        return jsonify(None)
    cur = mysql.connection.cursor()
    query_statement = f"UPDATE machines SET machine_name = '{name}', location = '{loc}' WHERE machine_id = {machine_id}"
    cur.execute(query_statement)
    mysql.connection.commit()
    cur.close()
    return jsonify(content)


@app.route('/item/', methods=['GET'])
def read_item():
    id = request.args.get("id")
    if id is None:
        return jsonify(None)
    cur = mysql.connection.cursor()
    query_statement = f"SELECT * from items WHERE item_id = {id}"
    result_value = cur.execute(query_statement)
    if result_value > 0:
        item = cur.fetchone()
        if request.method == 'GET':
            cur.close()
            return jsonify(item)
    return jsonify(None)


@app.route('/all-items/', methods=['GET'])
def read_all_items():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        query_statement = f"SELECT * from items"
        result = cur.execute(query_statement)
        if result > 0:
            items = cur.fetchall()
            cur.close()
            return jsonify(items)
    return jsonify(None)


@app.route('/item/create', methods=['POST'])
def create_item():
    if request.method == 'POST':
        content = request.get_json(silent=True)
        if content is None:
            return jsonify(None)
        cur = mysql.connection.cursor()
        try:
            name = content['item_name']
            price = int(content['price'])
        except KeyError and ValueError:
            return jsonify(None)
        query_statement = f"INSERT INTO items(item_name, price) VALUES ('{name}', {price})"
        cur.execute(query_statement)
        mysql.connection.commit()
        cur.close()
        # Maybe redirect
        return jsonify(content)
    return jsonify(None)


@app.route('/item/delete', methods=['POST'])
def delete_item():
    if request.method == 'POST':
        content = request.get_json(silent=True)
        if content is None:
            return jsonify(None)
        cur = mysql.connection.cursor()
        try:
            item_id = content['id']
        except KeyError:
            return jsonify(None)
        query_statement = f"DELETE from machine_products WHERE item_id = {item_id}"
        cur.execute(query_statement)  # Hoping for a better way to delete from both tables at once
        query_statement = f"DELETE from items WHERE item_id = {item_id}"
        cur.execute(query_statement)
        mysql.connection.commit()
        cur.close()
        # Maybe redirect
    return jsonify(None)


@app.route('/item/edit', methods=['POST'])
def edit_item():
    content = request.get_json(silent=True)
    if content is None:
        return jsonify(None)
    try:
        item_id = content['id']
        price = content['price']
    except KeyError:
        return jsonify(None)
    cur = mysql.connection.cursor()
    query_statement = f"UPDATE items SET price = '{price}' WHERE item_id = {item_id}"
    cur.execute(query_statement)
    mysql.connection.commit()
    cur.close()
    return jsonify(content)


if __name__ == '__main__':
    app.run(debug=True)
