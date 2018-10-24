"""
File contains funtions to register store owner and store attendant
"""
from flask import jsonify, session
from api.models import User
from api.utils.generate_id import create_id
from api.utils.validators import validate_register_data, validate_login_data


def register_user(data, db_users, is_admin):
    """
    Function to register store owner and attendant
    """
    # Get each field which was sent
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")

    # Validate input
    res = validate_register_data(first_name, last_name, email, password)
    if res:
        return res

    # Check if user already exists
    user = [u for u in db_users if u.email == email]
    if len(user) > 0:
        return jsonify({
            "error": "User with this email address already exists"
            }), 400

    user_id = create_id(db_users)
    new_user = User(user_id=user_id, first_name=first_name,
                    last_name=last_name, email=email, 
                    password=password, is_admin=is_admin)

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

    res = validate_login_data(email, password)
    if res:
        return res

    user = [u for u in db_users if u.email == email]
    if not user:
        return jsonify({"error": "Please register to login"}), 401
    
    # Check if it's a store owner and the password is theirs
    if is_admin and user[0].password == password:
        session["store_owner"] = email
        return jsonify({
            "message": "Store owner logged in successfully"
            })
    # Check if it's a store attendant and the password is theirs
    elif not is_admin and user[0].password == password:
        session["store_attendant"] = email
        return jsonify({
            "message": "Store attendant logged in successfully"
            })
    return jsonify({"error": "Invalid email or password"}), 401
