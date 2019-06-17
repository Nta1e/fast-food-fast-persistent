import json
import re

from flask import jsonify, request
from werkzeug.security import generate_password_hash

from ..models.models import Users


class HandleRegistration:

    def register_user(self):
        """This method handles the registration of a new user"""
        data = request.json
        given_data = {
            "username": data.get("username"),
            "email": data.get("email"),
            "password": data.get("password"),
            "confirm_password": data.get("confirm_password"),
            "admin": data.get("admin", False)
        }
        if not all(
            [data.get('username'),
            data.get('email'),
            data.get('password'),
            data.get('confirm_password')]
        ):
            return jsonify({'error': 'Missing field/s'}), 400
        try:
            int(given_data["username"])
            return jsonify({"error": "username cannot be an integer"}), 400
        except:
            pass
        if given_data["username"] is not None and given_data["username"].strip() == "":
            return jsonify({"error": "Required field/s Missing"}), 400
        if given_data["email"] is not None and given_data["email"].strip() == "":
            return jsonify({"error": "Required field/s Missing"}), 400
        if given_data["password"] is not None and given_data["password"].strip() == "":
            return jsonify({"error": "Required field/s Missing"}), 400
        if given_data["confirm_password"] is not None and given_data["confirm_password"].strip(
        ) == "":
            return jsonify({"error": "Required field/s Missing"}), 400
        if not re.match(r"[^@]+@[^@]+\.[^@]+", given_data["email"]):
            return jsonify({"error": "Invalid email"}), 400
        if given_data["password"] != given_data["confirm_password"]:
            return jsonify({"error": "Your passwords do not match!"}), 400
        if len(given_data["password"]) < 5:
            return jsonify({"error": "Password too short!"}), 400

        else:

            user = Users(
                given_data["username"],
                given_data["email"],
                generate_password_hash(given_data["password"], method='sha256'),
                given_data["admin"]
            )
            all_users = user.get_all_users()
            for each in all_users:
                if each["username"] == user.username:
                    return jsonify({"error": "Username already taken!"}), 409
                elif each["email"] == user.email:
                    return jsonify({"error": "Email already exists!"}), 409
            user.create_user()
            return jsonify({"message": "Registration Successfull"}), 201
