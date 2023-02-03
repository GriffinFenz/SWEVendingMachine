from flask import Blueprint, jsonify, Response

bp = Blueprint("app", __name__)


@bp.route("/")
def index() -> Response:
    return jsonify(success=True)
