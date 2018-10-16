from flask import jsonify, request
from flask.views import MethodView
from werkzeug.security import generate_password_hash, check_password_hash
from api.models import User
from api.__init__ import app

store_owners = []
class StoreOwnerRegister(MethodView):
    def post(self):
        data = request.get_json()

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        user_id = len(store_owners) + 1

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

        password = generate_password_hash(password)
        new_user = User(user_id, first_name, last_name, email, password, True)
        store_owners.append(new_user)

        return jsonify({"message": "Store owner successfully registered"}), 201


app.add_url_rule('/api/v1/store-owner/register', view_func=StoreOwnerRegister.as_view('users'))
