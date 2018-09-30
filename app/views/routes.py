from flask import Flask, jsonify, request, Blueprint
from ..models.models import Users, get_all_users, get_user_by_id, update_admin_status
from ..controllers import registration_controller, login_controller
from flask_jwt_extended import jwt_required, get_jwt_identity
JSON_MIME_TYPE = 'application/json'

admin = Blueprint("admin_route", __name__)
users = Blueprint("user_route", __name__)
auth = Blueprint("authentication", __name__)


@auth.route("/signup", methods=['POST'])
def signup():
    """This route handles registration of a new user"""
    if request.content_type != JSON_MIME_TYPE:
        return jsonify({"Error": "Invalid content_type"}), 400
    return registration_controller.register_user()


@auth.route("/login", methods=['POST'])
def login():
    """This route handles user login"""
    if request.content_type != JSON_MIME_TYPE:
        return jsonify({"Error": "Invalid content_type"}), 400
    return login_controller.signin()
