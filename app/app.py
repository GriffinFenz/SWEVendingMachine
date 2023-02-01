from flask import render_template, request, jsonify, Blueprint

bp = Blueprint("app", __name__)


@bp.route("/")
def index():
    return render_template("index.html")
