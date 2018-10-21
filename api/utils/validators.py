"""
File containig validators
"""

from flask import jsonify


def validate_product(name, price, quantity, category):
    """
    Funtion to validate product data
    """
    # Check if fields are empty
    if not name or not price or not quantity:
        return jsonify({
            "error": "Product name, price and quantity is required"
            }), 400

    return None
