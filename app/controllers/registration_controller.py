from flask import request, jsonify
from werkzeug.security import generate_password_hash
import re
import json
from ..models.models import Users, get_all_users


def register_user():
    """This method handles the registration of a new user"""
    data = request.json
    given_data = {
        "username": data.get("username"),
        "email": data.get("email"),
        "password": data.get("password"),
        "confirm_password": data.get("confirm_password"),
        "role": data.get("role")
    }
    if given_data["username"] is not None and given_data["username"].strip() == "":
        return jsonify({"error": "Required field/s Missing"}), 400
    if given_data["email"] is not None and given_data["email"].strip() == "":
        return jsonify({"error": "Required field/s Missing"}), 400
    if given_data["password"] is not None and given_data["password"].strip() == "":
        return jsonify({"error": "Required field/s Missing"}), 400
    if given_data["confirm_password"] is not None and given_data["confirm_password"].strip(
    ) == "":
        return jsonify({"error": "Required field/s Missing"}), 400
    if given_data["role"] is None:
        given_data["role"] = "user"
    if not re.match(r"[^@]+@[^@]+\.[^@]+", given_data["email"]):
        return jsonify({"error": "Invalid email"}), 400
    if given_data["password"] != given_data["confirm_password"]:
        return jsonify({"error": "Your passwords do not match!"}), 400
    if len(given_data["password"]) < 5:
        return jsonify({"error": "Password too short!"}), 400

    new_user = Users(
        given_data["username"].lower(),
        given_data["email"],
        generate_password_hash(given_data["password"], method='sha256'),
        given_data["role"]
    )
    all_users = get_all_users()
    for user in all_users:
        if user["username"] == new_user.username:
            return jsonify({"error": "Username already taken!"}), 409
        elif user["email"] == new_user.email:
            return jsonify({"error": "Email already exists!"}), 409
    new_user.create_user()
    return jsonify({"message": "Registration Successfull"}), 201
