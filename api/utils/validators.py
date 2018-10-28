"""
File containig validators
"""

from flask import jsonify
from validate_email import validate_email


def validate_register_data(**kwargs):
    """
    Function to validate registration data
    """
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


def validate_product(name, price, quantity):
    """
    Funtion to validate product data
    """
    # Check if fields are empty
    if not name or not price or not quantity:
        return jsonify({
            "error": "Product name, price and quantity is required"
            }), 400

    # Check for valid price and quantity input
    if not isinstance(price, int) or not isinstance(quantity, int):
        return jsonify({
            "error": "Product price and quantity must be integers"
            }), 400

    return None
