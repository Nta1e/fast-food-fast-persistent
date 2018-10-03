from flask import request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from ..models.models import Users, get_user
import datetime
import json


def signin():
    '''This function controlls user login'''

    data = request.json
    given_data = {
        "username": data.get("username"),
        "password": data.get("password")
    }
    if not given_data['username']:
        return jsonify({"Error": "Username missing!"}), 400

    if not given_data['password']:
        return jsonify({"Error": "Password missing"})
    '''checking if the user exists in the database'''
    client = get_user(given_data["username"])
    if client is None:
        return jsonify({"Error": "User does not exist!"}), 400
    elif check_password_hash(client["password"], given_data["password"]) is True:
        '''checking if the password is correct and giving the user an access token'''
        access_token = create_access_token(
            identity=client["id"], expires_delta=datetime.timedelta(hours=24))
        return jsonify({"message": "Login successfull!", "token": access_token}), 200
    return jsonify({"error": "password incorrect!"}), 401
