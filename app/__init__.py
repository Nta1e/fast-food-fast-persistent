from flask import Flask
from flask_jwt_extended import JWTManager
from .views.routes import admin, users, auth

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'my-beautiful-dark-twisted-fantasy'
jwt = JWTManager(app)

app.register_blueprint(admin, url_prefix="/api/v2/admin")
app.register_blueprint(users, url_prefix="/api/v2/users")
app.register_blueprint(auth, url_prefix="/api/v2/auth")
