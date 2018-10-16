"""
File contains decorators used in my app
"""
from functools import wraps
from flask import jsonify, session


def is_store_owner(f):
    """
    Authenticates if store owner is logged in
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if "store_owner" in session:
            return f(*args, **kwargs)
        return jsonify({
            "error": "Please login as a store owner to create a product"
            }), 401
    return decorated
