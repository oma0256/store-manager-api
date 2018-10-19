"""
File contains funtions to register store owner and store attendant
"""
from flask import jsonify, session
# from werkzeug.security import generate_password_hash, check_password_hash
# from validate_email import validate_email
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
    # confirm_password = data.get("confirm_password")

    # Check for empty fields
    if not first_name or not last_name or not password:
        return jsonify({"error": "This field is required"}), 400
    # if not last_name:
    #     return jsonify({"error": "Last name field is required"}), 400
    # if not email:
    #     return jsonify({"error": "Email field is required"}), 400
    # if not password:
    #     return jsonify({"error": "Password field is required"}), 400
    # if not confirm_password:
    #     return jsonify({"error": "Confirm password field is required"}), 400

    # # Validate email
    # is_valid = validate_email(email)
    # if not is_valid:
    #     return jsonify({"error": "Please enter a valid email"}), 400

    # # Check if passwords match
    # if password != confirm_password:
    #     return jsonify({"error": "The passwords must match"}), 400

    # Check if user already exists
    for user in db_users:
        if user.email == email:
            return jsonify({
                "error": "User with this email address already exists"
                }), 400

    # # Encrypt password
    # password = generate_password_hash(password)
    user_id = len(db_users) + 1
    new_user = User(user_id, first_name, last_name, email, password, is_admin)

    # Add user to list
    db_users.append(new_user)

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
    if not email:
        return jsonify({"error": "Email field is required"}), 400
    if not password:
        return jsonify({"error": "Password field is required"}), 400

    for user in db_users:
        # Check if the user is registered
        if user.email == email:
            # # Check if they input the correct password
            # if check_password_hash(user.password, password):
            if is_admin:
                session["store_owner"] = email
                return jsonify({
                    "message": "Store owner logged in successfully"
                    })
            session["store_attendant"] = email
            return jsonify({
                "message": "Store attendant logged in successfully"
                })
        return jsonify({"error": "Invalid email or password"}), 401
    return jsonify({"error": "Please register to login"}), 401
