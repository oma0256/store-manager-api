from flask import jsonify, request
from flask.views import MethodView
from flask_jwt_extended import (jwt_required, 
                                get_jwt_identity)
from api.models import Product
from api.__init__ import app
from api.utils.validators import validate_product
from db import DB


db_conn = DB()


class ProductView(MethodView):
    """
    Class to perform http methods on products
    """
    @jwt_required
    def post(self):
        """
        Handles creating of a product
        """
        # Get logged in user
        current_user = get_jwt_identity()
        loggedin_user = db_conn.get_user(current_user)
        # # Check if it's not store owner
        if not loggedin_user["is_admin"]:
            return jsonify({
                "error": "Please login as a store owner"
            }), 403

        res = validate_product(request)
        if res:
            return res
        
        data = request.get_json()
        # Get the fields which were sent
        name = data.get("name")
        unit_cost = data.get("unit_cost")
        quantity = data.get("quantity")
        category_id = data.get("category_id")


        # create a product object
        new_product = Product(name=name, unit_cost=unit_cost, 
                              quantity=quantity, category_id=category_id)
        # Check if product exists with this name
        product = db_conn.get_product_by_name(name)
        if product:
            return jsonify({
                "error": "Product with this name already exists"
            }), 400
        # Add product to database
        db_conn.add_product(new_product)
        return jsonify({
            "message": "Product created successfully",
            "product": db_conn.get_product_by_name(name)
            }), 201

    @jwt_required
    def get(self, product_id=None):
        """
        Get all products
        """
        # Check if an id has been passed
        if product_id:
            product = db_conn.get_product_by_id(int(product_id))
            # Check if product doesn't exist
            if not product:
                return jsonify({
                    "error": "This product does not exist"
                }), 404
            return jsonify({
                "message": "Product returned successfully",
                "product": product
                })
        # Get all products
        products = db_conn.get_products()
        return jsonify({
            "message": "Products returned successfully",
            "products": products
        })
    
    @jwt_required
    def put(self, product_id):
        """
        Funtion to modify a product
        """
        # Get logged in user
        current_user = get_jwt_identity()
        loggedin_user = db_conn.get_user(current_user)
        # # Check if it's not store owner
        if not loggedin_user["is_admin"]:
            return jsonify({
                "error": "Please login as a store owner"
            }), 403
        
        res = validate_product(request)
        if res:
            return res
        
        # Check if product exists
        product = db_conn.get_product_by_id(int(product_id))
        if not product:
            return jsonify({
                "error": "The product you're trying to modify doesn't exist"
            }), 404

        data = request.get_json()
        # Get the fields which were sent
        name = data.get("name")
        unit_cost = data.get("unit_cost")
        quantity = data.get("quantity")
        category_id = data.get("category_id")            
        
        # Modify product
        db_conn.update_product(name=name, unit_cost=unit_cost, quantity=quantity, 
                               product_id=int(product_id), category_id=category_id)
        return jsonify({
            "message": "Product updated successfully",
            "product": db_conn.get_product_by_id(product_id)
        })
    
    @jwt_required
    def delete(self, product_id):
        """
        Funtion to delete a product
        """
        # Get logged in user
        current_user = get_jwt_identity()
        loggedin_user = db_conn.get_user(current_user)
        # Check if it's not store owner
        if not loggedin_user["is_admin"]:
            return jsonify({
                "error": "Please login as a store owner"
            }), 403
        
        # Check if product exists
        product = db_conn.get_product_by_id(int(product_id))
        if not product:
            return jsonify({
                "error": "Product you're trying to delete doesn't exist"
            }), 404

        # Delete product
        db_conn.delete_product(int(product_id))
        return jsonify({
            "message": "Product has been deleted successfully"
        })


app.add_url_rule('/api/v2/products',
                 view_func=ProductView.as_view('product_view'),
                 methods=["GET", "POST"])
app.add_url_rule('/api/v2/products/<product_id>',
                 view_func=ProductView.as_view('product_view1'),
                 methods=["GET", "PUT", "DELETE"])
