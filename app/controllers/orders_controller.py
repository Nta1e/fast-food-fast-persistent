from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from ..models.models import Orders, get_menu_item, get_meal_id


def make_order(made_by):
    """This function handles the creation of a new order"""

    data = request.json
    user_id = get_jwt_identity()
    given_data = {
        "user_id": user_id,
        "order_made": data.get("order"),
        "location": data.get("location"),
        "comment": data.get("comment"),
        "made_by": made_by
    }
    if given_data["order_made"] is not None and given_data["order_made"].strip() == "":
        return jsonify({"error": "Required field/s Missing"}), 400
    if given_data["location"] is not None and given_data["location"].strip() == "":
        return jsonify({"error": "Required field/s Missing"}), 400
    if given_data["comment"] is not None and given_data["comment"].strip() == "":
        return jsonify({"error": "Required field/s Missing"}), 400
    item = get_menu_item(given_data["order_made"])
    if item is None:
        return jsonify(msg='item is not available on the menu!'), 400
    else:
        meal_id = get_meal_id(given_data["order_made"])
        new_order = Orders(
            given_data["user_id"],
            meal_id,
            given_data["order_made"].lower(),
            given_data["location"],
            given_data["comment"],
            given_data["made_by"]
        )
        order_dict = {
            "made_by": new_order.made_by,
            "order_made": new_order.order_made,
            "location": new_order.location,
            "comment": new_order.comment
        }
        new_order.create_order()
        return jsonify({"Message": "Order Created!"}, {"Order": order_dict}), 201
