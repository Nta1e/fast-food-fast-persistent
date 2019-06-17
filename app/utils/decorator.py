from functools import wraps

from flask import jsonify
from flask_jwt_extended import (JWTManager, get_jwt_identity,
                                verify_jwt_in_request)

from app.models.models import Users


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        client = Users().get_user_by_id(user_id)
        if not client["admin"]:
            msg='This url can only be accessed by an admin'
            return jsonify(msg), 403
        else:
            return f(*args, **kwargs)
    return wrapper
