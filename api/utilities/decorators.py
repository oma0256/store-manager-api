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
            "error": "Please login as a store owner"
            }), 401
    return decorated


def is_store_attendant(f):
    """
    Authenticates if store attendant is logged in
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if "store_attendant" in session:
            return f(*args, **kwargs)
        return jsonify({
            "error": "Please login as a store attendant"
            }), 401
    return decorated


def is_store_owner_or_attendant(f):
    """
    Authenticates if store attendant is logged in
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if "store_owner" in session or "store_attendant" in session:
            return f(*args, **kwargs)
        return jsonify({
            "error": "Please login as a store owner or attendant"
            }), 401
    return decorated
