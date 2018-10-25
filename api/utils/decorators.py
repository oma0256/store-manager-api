"""
File contains decorators used in my app
"""
from functools import wraps
from flask import jsonify, session


def is_store_owner_attendant(f, user, error_msg):
    """
    Authenticates if store owner or attendant is logged in
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Check if store owner or attendant is in session
        if user in session:
            return f(*args, **kwargs)
        return jsonify({
            "error": error_msg
            }), 401
    return decorated


def is_store_owner_or_attendant(f):
    """
    Authenticates if store attendant is logged in or owner
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if "store_owner" in session or "store_attendant" in session:
            return f(*args, **kwargs)
        return jsonify({
            "error": "Please login as a store owner or attendant"
            }), 401
    return decorated


def is_forbidden(f, user, error_msg):
    """
    Check if store attendant is looged in and store owner is not
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if user in session:
            return jsonify({
                "error": error_msg
                }), 403
        return f(*args, **kwargs)
    return decorated
