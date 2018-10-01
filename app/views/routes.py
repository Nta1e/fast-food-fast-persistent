from flask import Flask, jsonify, request, Blueprint
from ..models.models import (
    Users, get_all_users, get_user_by_id, update_admin_status, get_menu, get_username)
from ..controllers import (registration_controller,
                           login_controller, menu_controller, orders_controller)
from ..controllers.menu_controller import admin_required
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


@admin.route("/users", methods=['GET'])
@admin_required
def get_users():
    all_users = get_all_users()
    return jsonify({"users": all_users}), 200


@admin.route("/menu", methods=['POST'])
@admin_required
def add_meal():
    '''This route handles adding of a meal option to the menu'''
    if request.content_type != JSON_MIME_TYPE:
        return jsonify({"Error": "Invalid content_type"}), 400
    return menu_controller.add_meal_option()


@admin.route("/menu/<int:meal_id>", methods=['PUT'])
@admin_required
def edit_meal(meal_id):
    '''This route handles the editing of a meal option'''
    if request.content_type != JSON_MIME_TYPE:
        return jsonify({"Error": "Invalid content_type"}), 400
    return menu_controller.update_meal_option(meal_id)


@admin.route("/menu/<int:meal_id>", methods=['DELETE'])
@admin_required
def delete_meal(meal_id):
    '''This route handles the deleting of a meal option'''
    return menu_controller.remove_meal(meal_id)


@admin.route("/menu", methods=['GET'])
@admin_required
def view_menu():
    menu = get_menu()
    return jsonify({"menu": menu}), 200


@users.route("/menu", methods=['GET'])
@jwt_required
def see_menu():
    """This endpoint handles the viewing of the available menu by the user"""
    menu = get_menu()
    return jsonify({"menu": menu}), 200


@users.route("/orders", methods=['POST'])
@jwt_required
def place_order():
    '''This endpoint handles the placing of an order by the user'''
    if request.content_type != JSON_MIME_TYPE:
        return jsonify({"Error": "Invalid content_type"}), 400
    user_id = get_jwt_identity()
    username = get_username(user_id)
    return orders_controller.make_order(username)
