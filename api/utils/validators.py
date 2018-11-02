"""
File containig validators
"""
import re
from flask import jsonify
from validate_email import validate_email
from db import DB


int_partern = r"^[0-9]*$"
def validate_register_data(**kwargs):
    """
    Function to validate registration data
    """
    first_name = kwargs.get("first_name")
    last_name = kwargs.get("last_name")
    email = kwargs.get("email")
    password = kwargs.get("password")
    confirm_password = kwargs.get("confirm_password")
    # Check for empty fields
    if not first_name or not last_name or not email or not password or not confirm_password:
        return jsonify({
            "error": "First name, last name, email, password and confirm password fields are required"
            }), 400
    # Check if email is valid
    is_valid = validate_email(email)
    if not is_valid:
        return jsonify({
            "error": "Please use a valid email address"
        }), 400
    # Check if first and last name are alphabets only
    if not first_name.isalpha() or not last_name.isalpha():
        return jsonify({
            "error": "First and last name should only be alphabets"
        }), 400
    # Check if password and confirm password are equal
    if password != confirm_password:
        return jsonify({
            "error": "Passwords must match"
        }), 400


def validate_login_data(email, password):
    """
    Funtion to validate data to login a user
    """
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
    if not re.match(int_partern, str(unit_cost)) or not re.match(int_partern, str(quantity)):
        return jsonify({
            "error": "Product unit_cost and quantity must be integers"
            }), 400

    if category_id:
        if not re.match(int_partern, str(category_id)):
            return jsonify({
                "error": "Category id must be an integer"
                })

def validate_cart_item(product_id, quantity):
    """
    Function to validate cart item
    """
    db_conn = DB()
    # Check if fields are empty
    if not product_id or not quantity:
        return jsonify({
            "error": "Product id and quantity is required"
        }), 400
    
    # Check for valid product id and quantity
    if not re.match(int_partern, str(product_id)) or not re.match(int_partern, str(quantity)):
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
