from flask import Blueprint, jsonify, render_template, request

bp = Blueprint("app", __name__)


@bp.route("/")
def index():
    return render_template("index.html")
