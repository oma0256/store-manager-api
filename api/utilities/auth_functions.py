"""
File contains funtions to register store owner and store attendant
"""
from flask import jsonify, session
from api.models import User


def register_user(data, db_users, is_admin):
    """
    Function to register store owner and attendant
    """
    # Get each field which was sent
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")

    # Check for empty fields
    if not first_name or not last_name or not email or not password:
        return jsonify({"error": "This field is required"}), 400

    # Check if user already exists
    for user in db_users:
        if user.email == email:
            return jsonify({
                "error": "User with this email address already exists"
                }), 400

    user_id = len(db_users) + 1
    new_user = User(user_id, first_name, last_name, email, password, is_admin)

    # Add user to list
    db_users.append(new_user)

    # Check if is store owner or attendant
    if is_admin:
        return jsonify({"message": "Store owner successfully registered"}), 201
    return jsonify({"message": "Store attendant successfully registered"}), 201


def login_user(data, db_users, is_admin):
    """
    Function to login store owner and attendant
    """
    # Get fields which were sent
    email = data.get("email")
    password = data.get("password")

    # Check if any field is empty
    if not email or not password:
        return jsonify({"error": "This field is required"}), 400

    for user in db_users:
        # Check if the user is registered
        if user.email == email:
            # Check if password and it's store owner
            if is_admin and user.password == password:
                session["store_owner"] = email
                return jsonify({
                    "message": "Store owner logged in successfully"
                    })
            # Check if password and it's store attendant
            elif not is_admin and user.password == password:
                session["store_attendant"] = email
                return jsonify({
                    "message": "Store attendant logged in successfully"
                    })
            return jsonify({"error": "Invalid email or password"}), 401
    return jsonify({"error": "Please register to login"}), 401
