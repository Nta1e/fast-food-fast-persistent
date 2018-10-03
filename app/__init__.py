from flask import Flask, jsonify
from flasgger import Swagger
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .views.routes import admin, users, auth

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'my-beautiful-dark-twisted-fantasy'
jwt = JWTManager(app)
Swagger = Swagger(app)
app.register_blueprint(admin, url_prefix="/api/v2/admin")
app.register_blueprint(users, url_prefix="/api/v2/users")
app.register_blueprint(auth, url_prefix="/api/v2/auth")
