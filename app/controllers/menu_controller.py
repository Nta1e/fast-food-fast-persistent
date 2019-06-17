from flask import jsonify, request

from ..models.models import Menu


class HandleMenu:

    def __init__(self):
        self.data = request.json
        self.menu_item = self.data.get("menu_item")
        self.price = self.data.get("price")
        self.given_data = {
            "menu_item": self.menu_item.lower(),
            "price": self.price
        }
        self.menu = Menu(**self.given_data)
    def add_meal_option(self):
        # This function handles adding of a meal option onto the menu

        if self.given_data["menu_item"] is not None and \
            self.given_data["menu_item"].strip() == "":
            return jsonify({"Error": "Required field/s missing"}), 400
        if isinstance(self.given_data["price"], str):
            return jsonify({"Error": "Price has to be an integer"}), 400
        if not self.given_data["price"]:
            return jsonify({"Error": "Required field/s missing"}), 400
        full_menu = self.menu.get_menu()
        for meal in full_menu:
            if meal["menu_item"] == self.menu.menu_item:
                return jsonify({"error": "Meal already exists!"}), 409
        self.menu.add_item()
        return jsonify({"Message": "New meal added!",
                       "Meal": self.menu.__dict__}), 201

    def update_meal_option(self, meal_id):
        #This function handles the updating of a meal option
        meal = self.menu.get_meal_by_id(meal_id)
        if meal is None:
            return jsonify(error='Not found!'), 404
        data = request.json
        given_data = {
            "menu_item": data.get("menu_item"),
            "price": (data.get("price"))
        }
        if self.given_data["menu_item"] is not None and \
            self.given_data["menu_item"].strip() == "":
            return jsonify({"Error": "Required field/s missing"}), 400
        if isinstance(self.given_data["price"], str):
            return jsonify({"Error": "Price has to be an integer"}), 400
        if not self.given_data["price"]:
            return jsonify({"Error": "Required field/s missing"}), 400

        if not all(self.given_data):
            return jsonify({"Message": "No changes made!"},
                           {"Meal": self.menu.get_meal_by_id(meal_id)}), 200

        """Reverting back to original details if none is given"""
        if self.given_data['menu_item'] is None:
            self.menu_item = meal["menu_item"]
        if self.given_data['price'] is None:
            self.price = meal["price"]
        """updating the meal option"""
        self.menu.update_menu(meal_id, self.menu_item, self.price)
        return jsonify({"Message": "Menu updated!"},
                       {"Meal": self.menu.get_meal_by_id(meal_id)}), 201


    def remove_meal(self, meal_id):
        meal = self.menu.get_meal_by_id(meal_id)
        if meal is None:
            return jsonify({"error": "Not found"}), 404
        self.menu.delete_meal(meal_id)
        return jsonify(msg='Meal deleted!'), 200
