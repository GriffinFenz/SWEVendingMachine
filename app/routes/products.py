from flask import Blueprint, jsonify, request

from app.models.products import Products

product_bp = Blueprint("products", __name__)


@product_bp.route("/product", methods=["GET"])
def get_product():
    product_id = request.args.get("id")
    product = Products.find_by_id(product_id)
    return jsonify(Product=product, STATUS_CODE=200)


@product_bp.route("/all-products", methods=["GET"])
def get_all_products():
    return jsonify(Product=Products.query.all(), STATUS_CODE=200)


@product_bp.route("/product/create", methods=["POST"])
def create_product():
    content = request.get_json(silent=True)
    try:
        price = int(content["price"])
        product_name = content["product_name"]
    except KeyError:
        return jsonify(
            success=False,
            message="Missing price or/and product_name parameters",
            STATUS_CODE=400,
        )
    except ValueError:
        return jsonify(
            success=False,
            message="Price entered is not a valid number",
            STATUS_CODE=400,
        )
    # If product exist then return product else False run saying Product exists
    if Products.add_product(product_name, price):
        return jsonify(Product=Products.find_by_name(product_name), STATUS_CODE=200)
    return jsonify(success=False, message="Product already exists", STATUS_CODE=400)


@product_bp.route("/product/delete", methods=["DELETE"])
def delete_product():
    content = request.get_json(silent=True)
    try:
        product_id = content["product_id"]
    except KeyError:
        return jsonify(
            success=False, message="Missing product_id parameter", STATUS_CODE=400
        )
    # If product was deleted then show success message
    if Products.remove_product(product_id):
        return jsonify(
            success=True,
            message=f"Product with id: '{product_id}' has been deleted",
            STATUS_CODE=200,
        )
    return jsonify(
        success=False,
        message=f"No products that matches the id: '{product_id}'",
        STATUS_CODE=400,
    )


@product_bp.route("/product/edit", methods=["PUT"])
def edit_product():
    content = request.get_json(silent=True)
    try:
        product_id = content["product_id"]
        product_name = content["product_name"]
        price = int(content["price"])
    except KeyError:
        return jsonify(
            success=False,
            message="Missing product_id/price/product_name parameter",
            STATUS_CODE=400,
        )
    except ValueError:
        return jsonify(
            success=False,
            message="Price entered is not a valid number",
            STATUS_CODE=400,
        )
    output_check = Products.edit_product(product_id, product_name, price)
    if output_check == 2:
        return jsonify(
            success=False,
            message=f"Product with name: '{product_name}' already belongs in the database",
            STATUS_CODE=400,
        )
    if output_check == 1:
        return jsonify(
            success=False,
            message=f"Product with id: '{product_id}' does not exist",
            STATUS_CODE=400,
        )
    return jsonify(Product=Products.find_by_id(product_id), STATUS_CODE=200)
