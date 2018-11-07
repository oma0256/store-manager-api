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


def validate_product(name, unit_cost, quantity, category_id=None):
    """
    Funtion to validate product data
    """
    # Check if fields are empty
    if not name or not unit_cost or not quantity:
        return jsonify({
            "error": "Product name, unit_cost and quantity is required"
            }), 400

    if not name.isalpha():
        return jsonify({
            "error": "Product name must be a string"
            })

    # Check for valid unit_cost and quantity input
    if not isinstance(unit_cost, int) or not isinstance(quantity, int):
        return jsonify({
            "error": "Product unit_cost and quantity must be integers"
            }), 400

    if category_id:
        if not isinstance(category_id, int):
            return jsonify({
                "error": "Category id must be an integer"
                })
        category = db_conn.get_category_by_id(category_id)
        if not category:
            return jsonify({
                "error": "This category doesn't exist"
                }), 404

def validate_cart_item(product_id, quantity):
    """
    Function to validate cart item
    """
    # Check if fields are empty
    if not product_id or not quantity:
        return jsonify({
            "error": "Product id and quantity is required"
        }), 400
    
    # Check for valid product id and quantity
    if not type(product_id) is int or not type(quantity) is int:
        return jsonify({
            "error": "Product id and quantity must be integers"
            }), 400
    
    # Check if product exists in database
    product = db_conn.get_product_by_id(product_id)
    if not product:
        return jsonify({
            "error": "This product doesn't exist"
        }), 404
    
    # Check if quantity is more than product quantity in database
    if quantity > product["quantity"]:
        return jsonify({
            "error": "This product has only a quantity of " + str(product["quantity"])
            }), 400

def validate_data(request):
    try:
        data = request.get_json()
    except:
        return jsonify({"message": "Please check your inputs"}), 400
