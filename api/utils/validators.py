"""
File containig validators
"""

from flask import jsonify


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
