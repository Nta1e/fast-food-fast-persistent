from flask import Flask, jsonify, request, Blueprint
from ..models.models import (
    Users, get_all_users, get_user_by_id, update_admin_status, get_menu, get_username, get_user_orders,
    get_orders, get_order_by_id, insert_response)
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


@admin.route("/menu/<int:meal_id>/delete", methods=['DELETE'])
@admin_required
def delete_meal(meal_id):
    '''This route handles the deleting of a meal option'''
    return menu_controller.remove_meal(meal_id)


@admin.route("/menu", methods=['GET'])
@admin_required
def view_menu():
    admin_menu = get_menu()
    return jsonify({"menu": admin_menu}), 200


@users.route("/menu", methods=['GET'])
@jwt_required
def see_menu():
    """This endpoint handles the viewing of the available menu by the user"""
    user_menu = get_menu()
    return jsonify({"menu": user_menu}), 200


@users.route("/orders", methods=['POST'])
@jwt_required
def place_order():
    '''This endpoint handles the placing of an order by the user'''
    if request.content_type != JSON_MIME_TYPE:
        return jsonify({"Error": "Invalid content_type"}), 400
    user_id = get_jwt_identity()
    username = get_username(user_id)
    return orders_controller.make_order(username)


@users.route("/orders", methods=['GET'])
@jwt_required
def view_orders():
    '''This endpoint handles the viewing of user orders'''
    user_id = get_jwt_identity()
    username = get_username(user_id)
    user_orders = get_user_orders(username)
    return jsonify({"Your orders": user_orders}), 200


@admin.route("/orders", methods=['GET'])
@admin_required
def get_all_orders():
    '''This endpoint returns all the orders made'''
    all_orders = get_orders()
    return jsonify({"orders": all_orders}), 200


@admin.route("/orders/<int:order_id>", methods=['GET'])
@admin_required
def get_one_order(order_id):
    '''This endpoint returns one order'''
    one_order = get_order_by_id(order_id)
    return jsonify({"order": one_order}), 200


@admin.route("/orders/<int:order_id>/", methods=['PUT', 'GET'])
@admin_required
def update_status(order_id):
    '''This route handles updating of an order status'''
    if get_order_by_id(order_id) is None:
        return jsonify({"error": "Order not found!"}), 404

    status = request.json.get("Status")
    insert_response(status, order_id)
    return jsonify({"current_status": status}, {"order": get_order_by_id(order_id)}), 200
