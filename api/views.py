"""
File to handle application views
"""
from flask import jsonify, request, session
from flask.views import MethodView
from validate_email import validate_email
from werkzeug.security import generate_password_hash
from api.models import User
from api.__init__ import app

# Holds store owners
store_owners = []


class StoreOwnerRegister(MethodView):
    """
    Class to register store owner
    """
    def post(self):
        """
        Method that registers store owner
        """
        data = request.get_json()

        # Get each field which was sent
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        # Check for empty fields
        if not first_name:
            return jsonify({"error": "First name field is required"}), 400
        if not last_name:
            return jsonify({"error": "Last name field is required"}), 400
        if not email:
            return jsonify({"error": "Email field is required"}), 400
        if not password:
            return jsonify({"error": "Password field is required"}), 400
        if not confirm_password:
            return jsonify({"error": "Confirm password field is required"}), 400

        # Validate email
        is_valid = validate_email(email)
        if not is_valid:
            return jsonify({"error": "Please enter a valid email"}), 400

        # Check if passwords match
        if password != confirm_password:
            return jsonify({"error": "The passwords must match"}), 400

        # Check if user already exists
        for store_owner in store_owners:
            if store_owner.email == email:
                return jsonify({
                    "error": "User with this email address already exists"
                    }), 400

        # Encrypt password
        password = generate_password_hash(password)
        user_id = len(store_owners) + 1
        new_user = User(user_id, first_name, last_name, email, password, True)

        # Add user to list
        store_owners.append(new_user)
        return jsonify({"message": "Store owner successfully registered"}), 201


class StoreOwnerLogin(MethodView):
    def post(self):
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email:
            return jsonify({"error": "Email field is required"}), 400
        if not password:
            return jsonify({"error": "Password field is required"}), 400

        session["store_owner"] = email
        return jsonify({"message": "Store owner logged in successfully"})


# Map url to class
app.add_url_rule('/api/v1/store-owner/register',
                 view_func=StoreOwnerRegister.as_view('store_owner_register'))
app.add_url_rule('/api/v1/store-owner/login',
                 view_func=StoreOwnerLogin.as_view('store_owner_login'))
