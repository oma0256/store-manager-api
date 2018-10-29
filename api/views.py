"""
File to handle application views
"""
from functools import partial
from flask import jsonify, request, session
from flask.views import MethodView
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.models import Product, Sale, User
from api.__init__ import app
from api.utils.decorators import (is_store_owner_attendant,
                                  is_store_owner_or_attendant,
                                  is_forbidden)
from api.utils.auth_functions import register_user, login_user
from api.utils.validators import validate_product, validate_login_data, validate_register_data, validate_cart_item
from api.utils.generate_id import create_id
from db import DB



store_owner_decorator = partial(is_store_owner_attendant,
                                user="store_owner",
                                error_msg="Please login as a store owner")
store_attendant_decorator = partial(is_store_owner_attendant,
                                    user="store_attendant",
                                    error_msg="Please login as a store attendant")
not_store_owner = partial(is_forbidden,
                          user="store_attendant",
                          error_msg="Please login as a store owner")
not_store_attendant = partial(is_forbidden,
                              user="store_owner",
                              error_msg="Please login as a store attendant")

# Holds store owners
store_owners = []
# Hold store attendants
store_attendants = []
# Store products
products = []
# Store sales
sale_records = []


db_conn = DB()

@app.route("/")
def home_page():
    db_conn = DB()
    db_conn.create_admin()
    return "Welcome to the store manager"


class AppAuthView(MethodView):
    """
    Class to handle user authentication
    """
    def post(self):
        """
        handles registration and login
        """
        # check if it is store owner registration
        if request.path == '/api/v1/store-owner/register':
            return register_user(request.get_json(), store_owners, True)
        # check if it is store owner login
        if request.path == '/api/v1/store-owner/login':
            return login_user(request.get_json(), store_owners, True)
        # check if it is store attendant registration
        if request.path == '/api/v1/store-owner/attendant/register':
            return register_user(request.get_json(), store_attendants, False)
        # check if it is store attendant login
        if request.path == '/api/v1/store-attendant/login':
            return login_user(request.get_json(), store_attendants, False)


class LoginView(MethodView):
    """
    Class to login a user
    """
    def post(self):
        """
        Function to perform user login
        """
        # Get data sent
        db_conn = DB()
        data = request.get_json()
        # Get attributes of the data sent
        email = data.get("email")
        password = data.get("password")

        # Validate the data
        res = validate_login_data(email, password)
        if res:
            return res

        # Check if user already registered
        user = db_conn.get_user(email)
        if not user:
            return jsonify({"error": "Please register to login"}), 401

        # Check if it's a store owner and the password is theirs
        if user["is_admin"] and check_password_hash(user["password"], password):
            access_token = create_access_token(identity=email)
            return jsonify({
                "message": "Store owner logged in successfully",
                "token": access_token
                })
        # Check if it's a store attendant and the password is theirs
        if not user["is_admin"] and check_password_hash(user["password"], password):
            access_token = create_access_token(identity=email)
            return jsonify({
                "message": "Store attendant logged in successfully",
                "token": access_token
                })
        return jsonify({"error": "Invalid email or password"}), 401


class RegisterView(MethodView):
    """
    Class to handle adding a store attendant
    """
    @jwt_required
    def post(self):
        """
        Function to add a store attendant
        """
        db_conn = DB()

        # Get logged in user
        current_user = get_jwt_identity()
        loggedin_user = db_conn.get_user(current_user)
        # Check if it's not store owner
        if not loggedin_user["is_admin"]:
            return jsonify({
                "error": "Please login as store owner to add store attendant"
            }), 403

        # Get data sent
        data = request.get_json()
        # Get attributes of the data sent
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        # Validate the data
        res = validate_register_data(first_name=first_name, last_name=last_name, email=email, 
                                     password=password, confirm_password=confirm_password)
        if res:
            return res
        
        # Check if user is already registered
        user_exists = db_conn.get_user(email)
        if user_exists:
            return jsonify({
                "error": "User with this email already exists"
            }), 400

        new_user = User(first_name=first_name, last_name=last_name, 
                        email=email, password=generate_password_hash(password))
        # Add user to database
        db_conn.create_user(new_user)
        return jsonify({
            "message": "Store attendant added successfully"
        }), 201


class ProductView(MethodView):
    """
    Class to perform http methods on products
    """
    @jwt_required
    def post(self):
        """
        Handles creating of a product
        """
        db_conn = DB()

        # Get logged in user
        current_user = get_jwt_identity()
        loggedin_user = db_conn.get_user(current_user)
        # # Check if it's not store owner
        if not loggedin_user["is_admin"]:
            return jsonify({
                "error": "Please login as a store owner"
            }), 403
        
        data = request.get_json()
        # Get the fields which were sent
        name = data.get("name")
        unit_cost = data.get("unit_cost")
        quantity = data.get("quantity")
        # validates product and returns json response and status code
        res = validate_product(name=name, unit_cost=unit_cost, quantity=quantity)
        if res:
            return res

        # create a product object
        new_product = Product(name=name, unit_cost=unit_cost, quantity=quantity)
        # Check if product exists with this name
        product = db_conn.get_product_by_name(name)
        if product:
            return jsonify({
                "error": "Product with this name already exists"
            }), 400
        # Add product to database
        db_conn.add_product(new_product)
        return jsonify({
            "message": "Product created successfully",
            }), 201

    @jwt_required
    def get(self, product_id=None):
        """
        Get all products
        """
        db_conn = DB()
        # Check if an id has been passed
        if product_id:
            product = db_conn.get_product_by_id(int(product_id))
            # Check if product doesn't exist
            if not product:
                return jsonify({
                    "error": "This product does not exist"
                }), 404
            return jsonify({
                "message": "Product returned successfully"
                })
        # Get all products
        db_conn.get_products()
        return jsonify({
            "message": "Products returned successfully"
        })
    
    @jwt_required
    def put(self, product_id):
        """
        Funtion to modify a product
        """
        db_conn = DB()

        # Get logged in user
        current_user = get_jwt_identity()
        loggedin_user = db_conn.get_user(current_user)
        # # Check if it's not store owner
        if not loggedin_user["is_admin"]:
            return jsonify({
                "error": "Please login as a store owner"
            }), 403
        
        # Check if product exists
        product = db_conn.get_product_by_id(int(product_id))
        if not product:
            return jsonify({
                "error": "The product you're trying to modify doesn't exist"
            }), 404

        data = request.get_json()
        # Get the fields which were sent
        name = data.get("name")
        unit_cost = data.get("unit_cost")
        quantity = data.get("quantity")
        # validates product and returns json response and status code
        res = validate_product(name, unit_cost, quantity)
        if res:
            return res
        
        # Modify product
        db_conn.update_product(name, unit_cost, quantity, int(product_id))
        return jsonify({
            "message": "Product updated successfully"
        })
    
    @jwt_required
    def delete(self, product_id):
        """
        Funtion to delete a product
        """
        db_conn = DB()

        # Get logged in user
        current_user = get_jwt_identity()
        loggedin_user = db_conn.get_user(current_user)
        # Check if it's not store owner
        if not loggedin_user["is_admin"]:
            return jsonify({
                "error": "Please login as a store owner"
            }), 403
        
        # Check if product exists
        product = db_conn.get_product_by_id(int(product_id))
        if not product:
            return jsonify({
                "error": "Product you're trying to delete doesn't exist"
            }), 404

        # Delete product
        db_conn.delete_product(int(product_id))
        return jsonify({
            "message": "Product has been deleted successfully"
        })



class SaleView(MethodView):
    """
    Class to perform http methods on sales
    """
    @jwt_required
    def post(self):
        """
        Method to create a sale record
        """
        db_conn = DB()

        # Get logged in user
        current_user = get_jwt_identity()
        loggedin_user = db_conn.get_user(current_user)
        # Check if it's a store owner
        if loggedin_user["is_admin"]:
            return jsonify({
                "error": "Please login as a store attendant"
            }), 403

        data = request.get_json()
        # get items being sold
        cart_items = data.get("cart_items")
        total = 0
        product_names = ""
        for cart_item in cart_items:
            product_id = cart_item.get("product")
            quantity = cart_item.get("quantity")
            # validate each product
            res = validate_cart_item(product_id, quantity)
            if res:
                return res
            # Get product
            product = db_conn.get_product_by_id(product_id)
            if not product:
                return jsonify({
                    "error": "This product doesn't exist"
                    }), 404
            product_names += product["name"] + " "
            total += product["unit_cost"]
        current_user = get_jwt_identity()
        # Get attendant
        attendant = db_conn.get_user(current_user)
        db_conn.add_sale(int(attendant["id"]), product_names, total)
        return jsonify({
            "message": "Sale made successfully"
        }), 201

    @jwt_required
    def get(self, sale_id=None):
        """
        Perform GET on sale records
        """
        db_conn = DB()
        # Get current user
        current_user = get_jwt_identity()
        user = db_conn.get_user(current_user)
        # run if request is for a single sale record
        if sale_id:
            # Get a single sale record
            sale_record = db_conn.get_single_sale(int(sale_id))
            # # Check if sale doesn't exist
            if not sale_record:
                return jsonify({
                    "error": "Sale record with this id doesn't exist"
                }), 404
            # run if it's a store owner
            if user["is_admin"]:
                return jsonify({
                    "message": "Sale record returned successfully"
                    })
            # run if it's a store attendant
            if sale_record["attendant"] == db_conn.get_user(current_user)["id"]:
                return jsonify({
                    "message": "Sale record returned successfully"
                    })
            return jsonify({"error": "You didn't make this sale"}), 403
        # run if request is for all sale records and if it's a store
        # owner
        if user["is_admin"]:
            sale_records = db_conn.get_sale_records()
            return jsonify({
                "message": "Sale records returned successfully"
            })
        return jsonify({"error": "Please login as a store owner"}), 403


# Map urls to view classes
view = not_store_owner(store_owner_decorator(AppAuthView.as_view('store_attendant_register')))
app.add_url_rule('/api/v2/auth/login',
                 view_func=LoginView.as_view('login_view'))
app.add_url_rule('/api/v2/auth/signup',
                 view_func=RegisterView.as_view('register_view'))
app.add_url_rule('/api/v1/store-owner/register',
                 view_func=AppAuthView.as_view('store_owner_register'))
app.add_url_rule('/api/v1/store-owner/login',
                 view_func=AppAuthView.as_view('store_owner_login'))
app.add_url_rule('/api/v1/store-owner/attendant/register',
                 view_func=view)
app.add_url_rule('/api/v1/store-attendant/login',
                 view_func=AppAuthView.as_view('store_attendant_login'))
app.add_url_rule('/api/v2/products',
                 view_func=ProductView.as_view('product_view'),
                 methods=["GET", "POST"])
app.add_url_rule('/api/v2/products/<product_id>',
                 view_func=ProductView.as_view('product_view1'),
                 methods=["GET", "PUT", "DELETE"])
app.add_url_rule('/api/v2/sales',
                 view_func=SaleView.as_view('sale_view'),
                 methods=["GET","POST"])
app.add_url_rule('/api/v1/sales/<sale_id>',
                 view_func=SaleView.as_view('sale_view1'), methods=["GET"])
