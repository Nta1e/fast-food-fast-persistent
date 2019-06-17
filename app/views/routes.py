from flasgger import swag_from
from flask import Blueprint, Flask, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..controllers.login_controller import HandleLogin
from ..controllers.menu_controller import HandleMenu
from ..controllers.orders_controller import HandleOrders
from ..controllers.registration_controller import HandleRegistration
from ..models.models import Menu, Orders, Users
from ..utils.decorator import admin_required

JSON_MIME_TYPE = 'application/json'

admin = Blueprint("admin_route", __name__)
users = Blueprint("user_route", __name__)
auth = Blueprint("authentication", __name__)


@auth.route("/signup", methods=['POST'])
@swag_from('../docs/signup.yml')
def signup():
    """This route handles registration of a new user"""
    if request.content_type != JSON_MIME_TYPE:
        return jsonify({"Error": "Invalid content_type"}), 400
    return HandleRegistration().register_user()


@auth.route("/login", methods=['POST'])
@swag_from('../docs/login.yml')
def login():
    """This route handles user login"""
    if request.content_type != JSON_MIME_TYPE:
        return jsonify({"Error": "Invalid content_type"}), 400
    return HandleLogin().signin()


@admin.route("/users", methods=['GET'])
@swag_from('../docs/users.yml')
@admin_required
def get_users():
    '''This route returns all the users in the database'''
    all_users = Users().get_all_users()
    return jsonify({"users": all_users}), 200


@admin.route("/menu", methods=['POST'])
@swag_from('../docs/meals/add_meal.yml')
@admin_required
def add_meal():
    '''This route handles adding of a meal option to the menu'''
    if request.content_type != JSON_MIME_TYPE:
        return jsonify({"Error": "Invalid content_type"}), 400
    return HandleMenu().add_meal_option()


@admin.route("/menu/<int:meal_id>", methods=['PUT'])
@swag_from('../docs/meals/edit_menu.yml')
@admin_required
def edit_meal(meal_id):
    '''This route handles the editing of a meal option'''
    if request.content_type != JSON_MIME_TYPE:
        return jsonify({"Error": "Invalid content_type"}), 400
    return HandleMenu().update_meal_option(meal_id)


@admin.route("/menu/<int:meal_id>/delete", methods=['DELETE'])
@swag_from('../docs/meals/delete_meal.yml')
@admin_required
def delete_meal(meal_id):
    '''This route handles the deleting of a meal option'''
    return HandleMenu().remove_meal(meal_id)


@users.route("/menu", methods=['GET'])
@jwt_required
@swag_from('../docs/user_view_menu.yml')
def see_menu():
    """This endpoint handles the viewing of the available menu by the user"""
    available_menu = Menu().get_menu()
    return jsonify({"menu": available_menu}), 200


@users.route("/orders", methods=['POST'])
@jwt_required
@swag_from('../docs/orders/add_order.yml')
def place_order():
    '''This endpoint handles the placing of an order by the user'''
    if request.content_type != JSON_MIME_TYPE:
        return jsonify({"Error": "Invalid content_type"}), 400
    user_id = get_jwt_identity()
    username = Users().get_username(user_id)
    return HandleOrders().make_order(username)


@users.route("/orders", methods=['GET'])
@jwt_required
@swag_from('../docs/orders/view_orders.yml')
def view_orders():
    '''This endpoint handles the viewing of user orders'''
    user_id = get_jwt_identity()
    username = Users().get_username(user_id)
    user_orders = Orders().get_user_orders(username)
    return jsonify({"Your orders": user_orders}), 200


@admin.route("/orders", methods=['GET'])
@swag_from('../docs/orders/view_all_orders.yml')
@admin_required
def get_all_orders():
    '''This endpoint returns all the orders made'''
    all_orders = Orders().get_orders()
    return jsonify({"orders": all_orders}), 200


@admin.route("/orders/<int:order_id>", methods=['GET'])
@swag_from('../docs/orders/view_one.yml')
@admin_required
def get_one_order(order_id):
    '''This endpoint returns one order'''
    if Orders().get_order_by_id(order_id) is None:
        return jsonify({"error": "Order not found!"}), 404
    one_order = Orders().get_order_by_id(order_id)
    return jsonify({"order": one_order}), 200


@admin.route("/orders/<int:order_id>", methods=['PUT'])
@swag_from('../docs/orders/update_status.yml')
@admin_required
def update_status(order_id):
    '''This route handles updating of an order status'''
    if Orders().get_order_by_id(order_id) is None:
        return jsonify({"error": "order not found!"}), 404
    status_list = ["Processing", "Cancelled", "Complete"]
    status = request.json.get("status")
    if status not in status_list:
        return jsonify({"error": "Add correct status"}), 405
    Orders().insert_response(status, order_id)
    return jsonify({"current_status": status},
                   {"order": Orders().get_order_by_id(order_id)}), 200
