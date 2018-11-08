from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import (jwt_required, 
                                get_jwt_identity)
from api.models import Category
from api.__init__ import app
from api.utils.validators import validate_category
from db import DB


db_conn = DB()

class CategoryView(MethodView):
    """
    Handles http methods on category
    """

    @jwt_required
    def post(self):
        """
        Function to create category
        """
        # Get logged in user
        current_user = get_jwt_identity()
        user = db_conn.get_user(current_user)
        # Check if it's store attendant
        if not user["is_admin"]:
            return jsonify({
                "error": "Please login as a store owner"
            }), 403
        res = validate_category(request)
        if res:
            return res
        # Get data sent
        data = request.get_json()
        name = data.get("name")
        description = data.get("description")
        # Get a specific category
        category = db_conn.get_category_by_name(name)
        new_category = Category(name, description=description)
        # Add category to database
        db_conn.add_category(new_category)
        return jsonify({
            "message": "Successfully created product category",
            "category": db_conn.get_category_by_name(name)
        }), 201

    @jwt_required
    def put(self, category_id):
        """
        Function to modify a category
        """
        # Get logged in user
        current_user = get_jwt_identity()
        loggedin_user = db_conn.get_user(current_user)
        # # Check if it's not store owner
        if not loggedin_user["is_admin"]:
            return jsonify({
                "error": "Please login as a store owner"
            }), 403
        
        # Check if category exists
        category = db_conn.get_category_by_id(int(category_id))
        if not category:
            return jsonify({
                "error": "The category you're trying to modify doesn't exist"
            }), 404

        data = request.get_json()
        # Get the fields which were sent
        name = data.get("name")
        description = data.get("description")
        if not name:
            return jsonify({
                "error": "The category name is required"
            }), 400
        
        # Modify category
        db_conn.update_category(name, description, category_id)
        return jsonify({
            "message": "Category updated successfully",
            "category": db_conn.get_category_by_id(int(category_id))
        })

    @jwt_required
    def delete(self, category_id):
        """
        Funtion to category a product
        """
        # Get logged in user
        current_user = get_jwt_identity()
        loggedin_user = db_conn.get_user(current_user)
        # Check if it's not store owner
        if loggedin_user["is_admin"]:
            # Check if category exists
            category = db_conn.get_category_by_id(int(category_id))
            if not category:
                return jsonify({
                    "error": "Category you're trying to delete doesn't exist"
                }), 404

            # Delete category
            db_conn.delete_category(int(category_id))
            return jsonify({
                "message": "Category has been deleted successfully"
            })
        return jsonify({
            "error": "Please login as a store owner"
        }), 403


app.add_url_rule('/api/v2/categories',
                 view_func=CategoryView.as_view('category_view'),
                 methods=["POST"])
app.add_url_rule('/api/v2/categories/<category_id>',
                 view_func=CategoryView.as_view('category_view1'), 
                 methods=["PUT", "DELETE"])
