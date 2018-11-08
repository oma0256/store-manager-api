"""
File containig validators
"""
from flask import jsonify
from validate_email import validate_email
from db import DB


db_conn = DB()
def validate_register_data(request):
    """
    Function to validate registration data
    """
    res = validate_data(request)
    if res:
        return res
    data = request.get_json()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    # Check for empty fields
    if not first_name or not last_name or not first_name.isalpha() or not last_name.isalpha():
        return jsonify({
            "error": "First name and last name are required and must be alphabets"
            }), 400
    # Check if email is valid
    is_valid = validate_email(email)
    if not email or not is_valid:
        return jsonify({
            "error": "Please use a valid email address"
        }), 400
    # Check if password and confirm password are equal
    if not password or not confirm_password or password != confirm_password:
        return jsonify({
            "error": "Passwords are required and must match"
        }), 400


def validate_login_data(request):
    """
    Funtion to validate data to login a user
    """
    res = validate_data(request)
    if res:
        return res
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    # Check for empty fields
    if not email or not password:
        return jsonify({
            "error": "Email and password is required"
            }), 400
    return None


def validate_product(request):
    """
    Funtion to validate product data
    """
    data = request.get_json()
    # Get the fields which were sent
    name = data.get("name")
    unit_cost = data.get("unit_cost")
    quantity = data.get("quantity")
    category_id = data.get("category_id")
    if not name or not name.isalpha():
        return jsonify({
            "error": "Product name is required and must be alphabets"
            }), 400

    # Check for valid unit_cost and quantity input
    if not unit_cost or not isinstance(unit_cost, int) or unit_cost <= 0:
        return jsonify({
            "error": "Product unit cost is required and must be a positive integer"
            }), 400
    
    if not quantity or not type(quantity) is int or quantity <= 0:
        return jsonify({
            "error": "Product quantity is required and must be a positive integer"
            }), 400

    if category_id:
        error_msg = None
        if not isinstance(category_id, int) or category_id <= 0:
            error_msg = {"error": "Category id must be a positive integer"}
            status_code = 400
        elif not db_conn.get_category_by_id(int(category_id)):
            error_msg = {"error": "This category doesn't exist"}
            status_code = 404
        if error_msg:
            return jsonify(error_msg), status_code

def validate_cart_item(request):
    """
    Function to validate cart item
    """
    res = validate_data(request)
    if res:
        return res
    
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity")
    error_msg = None
    status_code = 200
    # Check if fields are empty
    if not product_id or not quantity:
        error_msg = {"error": "Product id and quantity is required"}
        status_code = 400
    
    # Check for valid product id and quantity
    elif not type(product_id) is int or product_id <= 0 or not type(quantity) is int or quantity <= 0:
        error_msg = {"error": "Product id and quantity must be positive integers"}
        status_code = 400
    
    # Check if product exists in database
    elif not db_conn.get_product_by_id(int(product_id)):
        error_msg = {"error": "This product doesn't exist"}
        status_code = 404
    
    # Check if quantity is more than product quantity in database
    elif quantity > db_conn.get_product_by_id(int(product_id))["quantity"]:
        error_msg = {"error": "This product has only a quantity of " + str(db_conn.get_product_by_id(int(product_id))["quantity"])}
        status_code = 400
    if error_msg:
        return jsonify(error_msg), status_code

def validate_category(request):
    res = validate_data(request)
    if res:
        return res
    # Get data sent
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    # Check if name is empty
    if not name:
        return jsonify({
            "error": "The category name is required"
        }), 400
    # Get a specific category
    category = db_conn.get_category_by_name(name)
    # Check if the category exists with that name
    if category:
        return jsonify({
            "error": "Category with this name exists"
        }), 400

def validate_data(request):
    try:
        data = request.get_json()
    except:
        return jsonify({"error": "Please check your inputs"}), 400
