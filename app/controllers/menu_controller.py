from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import (
    JWTManager, verify_jwt_in_request, get_jwt_identity
)
from ..models.models import (
    Menu, get_menu, update_menu, get_meal_by_id, delete_meal, get_user_by_id, get_admin_status)


def add_meal_option():
    """This function handles adding of a meal option onto the menu"""
    data = request.json
    given_data = {
        "menu_item": data.get("menu_item"),
        "price": (data.get("price"))
    }
    if given_data["menu_item"] is not None and given_data["menu_item"].strip() == "":
        return jsonify({"Error": "Required field/s missing"}), 400
    if isinstance(given_data["price"], str):
        return jsonify({"Error": "Price has to be an integer"}), 400
    if not given_data["price"]:
        return jsonify({"Error": "Required field/s missing"}), 400
    new_meal = Menu(
        given_data["menu_item"],
        given_data["price"]
    )
    entire_menu = get_menu()
    for item in entire_menu:
        if item["menu_item"] == new_meal.menu_item:
            return jsonify({"error": "Meal already exists!"}), 409
    new_meal.add_item()
    return jsonify({"Message": "New meal added!", "Meal": new_meal.__dict__}), 201


def update_meal_option(meal_id):
    """This function handles the updating of a meal option"""
    meal = get_meal_by_id(meal_id)
    if meal is None:
        return jsonify(error='Not found!'), 404
    data = request.json
    given_data = {
        "menu_item": data.get("menu_item"),
        "price": (data.get("price"))
    }
    if given_data["menu_item"] is not None and given_data["menu_item"].strip() == "":
        return jsonify({"Error": "Required field/s missing"}), 400
    if isinstance(given_data["price"], str):
        return jsonify({"Error": "Price has to be an integer"}), 400
    if not given_data["price"]:
        return jsonify({"Error": "Required field/s missing"}), 400

    menu_item = given_data["menu_item"]
    price = given_data["price"]
    if not all(given_data):
        return jsonify({"Message": "No changes made!"}, {"Meal": get_meal_by_id(meal_id)}), 200

    """Reverting back to original details if none is given"""
    if menu_item is None:
        menu_item = meal["menu_item"]
    if price is None:
        price = meal["price"]

    """updating the meal option"""
    update_menu(meal_id, menu_item, price)
    return jsonify({"Message": "Menu updated!"}, {"Meal": get_meal_by_id(meal_id)}), 201


def remove_meal(meal_id):
    meal = get_meal_by_id(meal_id)
    if meal is None:
        return jsonify({"error": "Not found"}), 404
    delete_meal(meal_id)
    return jsonify(msg='Meal deleted!'), 200

'''
Here Iam creating a custom decorator which will be used for endpoints restricted
to admin only
'''


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        client = get_user_by_id(user_id)
        if client["role"] == "user":
            return jsonify(msg='Admins only!'), 403
        else:
            return f(*args, **kwargs)
    return wrapper
