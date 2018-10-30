"""
Set up flask
"""

from flask import Flask
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.secret_key = 'super secret key'


# Setup flask-jwt-extended
app.config['JWT_SECRET_KEY'] = 'sajsvhca'
app.config.from_object("config.DevelopmentConfig")
jwt = JWTManager(app)

from api import views
