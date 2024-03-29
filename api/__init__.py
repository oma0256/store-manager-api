"""
Set up flask
"""

from flask import Flask
from flask_jwt_extended import JWTManager



def create_app(config_name):
    app = Flask(__name__)
    # Setup flask-jwt-extended
    app.config['JWT_SECRET_KEY'] = 'sajsvhca'
    app.config.from_object(config_name)
    jwt = JWTManager(app)
    return app

app = create_app('config.TestConfig')


from api import auth_views, products_views, category_views, sales_views
