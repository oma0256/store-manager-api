"""
File containig validators
"""

from flask import jsonify


def validate_product(name, price, quantity, category):
    """
    Funtion to validate product data
    """
    # Check if fields are empty
    if not name:
        return jsonify({"error": "Product name is required"}), 400
    if not price:
        return jsonify({"error": "Product price is required"}), 400
    if not quantity:
        return jsonify({"error": "Product quantity is required"}), 400
    if not category:
        return jsonify({"error": "Product category is required"}), 400

    # Check for invalid price or quantity
    if not isinstance(price, int) or not isinstance(price, int):
        return jsonify({"error": "Please enter an integer"}), 400

    return None
