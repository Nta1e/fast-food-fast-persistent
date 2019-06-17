from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity

from ..models.models import Menu, Orders


class HandleOrders:

    def __init__(self):
        self.user_id = get_jwt_identity()
        self.data = request.json
        self.order_made = self.data.get("order")
        self.location = self.data.get("location")
        self.comment = self.data.get("comment")
        self.menu = Menu()
        
    def make_order(self, made_by):
        """This function handles the creation of a new order"""
        given_data = {
            "user_id": self.user_id,
            "meal_id": self.menu.get_meal_id(self.order_made),
            "order_made": self.order_made,
            "location": self.location,
            "comment": self.comment,
            "made_by": made_by
        }
        if given_data["order_made"] is not None and \
            given_data["order_made"].strip() == "":
            return jsonify({"error": "Required field/s Missing"}), 400
        if given_data["location"] is not None and \
            given_data["location"].strip() == "":
            return jsonify({"error": "Required field/s Missing"}), 400
        if given_data["comment"] is not None and \
            given_data["comment"].strip() == "":
            return jsonify({"error": "Required field/s Missing"}), 400
        item = self.menu.get_menu_item(given_data["order_made"])
        if item is None:
            return jsonify(msg='item is not available on the menu!'), 400
        else:
            order = Orders(**given_data)
            order_dict = {
                "made_by": order.made_by,
                "order_made": order.order_made,
                "location": order.location,
                "comment": order.comment
            }
            order.create_order()
            return jsonify({"Message": "Order Created!"}, {"Order": order_dict}), 201
