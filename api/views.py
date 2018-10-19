"""
File to handle application views
"""
from flask import jsonify, request, session
from flask.views import MethodView
from api.models import Product, Sale
from api.__init__ import app
from api.utilities.decorators import (is_store_owner,
                                      is_store_owner_or_attendant,
                                      is_store_attendant,
                                      is_not_store_owner,
                                      is_not_store_attendant)
from api.utilities.auth_functions import register_user, login_user
from api.utilities.validators import validate_product
from functools import partial

store_owner_decorator = partial(is_store_owner, admin=True)
store_attendant_decorator = partial(is_store_owner, admin=False)

# Holds store owners
store_owners = []
# Hold store attendants
store_attendants = []
# Store products
products = []
# Store sales
sale_records = []


def get_single_resource(resource_list, resource_id, msg, key):
    for resource in resource_list:
        # check if sale record exists
        if resource.id == int(resource_id):
            return jsonify({
                "message": msg,
                key: resource.__dict__
            })
    if key == "products":
        return jsonify({"error": "This product does not exist"}), 404
    if key == 'sale':
        return jsonify({"error": "Sale record with this id doesn't exist"}), 404


class AppAuthView(MethodView):
    """
    Class to handle user authentication
    """
    def post(self):
        """
        handles registration and login
        """
        # check if it is store owner registration
        if request.path == '/api/v1/store-owner/register':
            return register_user(request.get_json(), store_owners, True)
        # check if it is store owner login
        if request.path == '/api/v1/store-owner/login':
            return login_user(request.get_json(), store_owners, True)
        # check if it is store attendant registration
        if request.path == '/api/v1/store-owner/attendant/register':
            return register_user(request.get_json(), store_attendants, False)
        # check if it is store attendant login
        if request.path == '/api/v1/store-attendant/login':
            return login_user(request.get_json(), store_attendants, False)


class ProductView(MethodView):
    """
    Class to perform http methods on products
    """
    @is_not_store_owner
    @store_owner_decorator
    def post(self):
        """
        Handles creating of a product
        """
        data = request.get_json()
        # Get the fields which were sent
        name = data.get("name")
        price = data.get("price")
        quantity = data.get("quantity")
        category = data.get("category")
        # validates product and returns json response and status code
        res = validate_product(name, price, quantity, category)
        if res:
            return res

        product_id = len(products) + 1
        # create a product object
        new_product = Product(product_id, name, price, quantity, category)
        # appends the product object to list
        products.append(new_product)
        return jsonify({
            "message": "Product created successfully",
            "product": new_product.__dict__
            }), 201

    @is_store_owner_or_attendant
    def get(self, product_id=None):
        """
        Get all products
        """
        # Check if an id has been passed
        if product_id:
            return get_single_resource(products, product_id,
                                       "Product returned successfully",
                                       "products")
        return jsonify({
            "message": "Products returned successfully",
            "products": [product.__dict__ for product in products]
        })


class SaleView(MethodView):
    """
    Class to perform http methods on sales
    """
    @is_not_store_attendant
    @store_attendant_decorator
    def post(self):
        """
        Method to create a sale record
        """
        data = request.get_json()
        # get items being sold
        cart_items = data.get("cart_items")
        total = 0
        for cart_item in cart_items:
            name = cart_item.get("name")
            price = cart_item.get("price")
            quantity = cart_item.get("quantity")
            category = cart_item.get("category")
            # validate each product
            res = validate_product(name, price, quantity, category)
            if res:
                return res
            total += price
        sale_id = len(sale_records) + 1
        attendant_name = ""
        for store_attendant in store_attendants:
            if store_attendant.email == session["store_attendant"]:
                attendant_name = store_attendant.first_name + " " + store_attendant.last_name
                attendant_email = session["store_attendant"]
                sale = Sale(sale_id, cart_items, attendant_name, attendant_email, total)
                sale_records.append(sale)
                return jsonify({
                    "message": "Sale created successfully",
                    "sale": sale.__dict__
                }), 201

    def get(self, sale_id=None):
        """
        Perform GET on sale records
        """
        # run if request is for a single sale record
        if sale_id:
            # run if it's a store owner
            if "store_owner" in session:
                return get_single_resource(sale_records, sale_id,
                                           "Sale record returned successfully",
                                           "sale")
            # run if it's a store attendant
            elif "store_attendant" in session:
                for sale_record in sale_records:
                    # check if sale record exists
                    if sale_record.attendant_email == session["store_attendant"]:
                        return get_single_resource(sale_records, sale_id,
                                                   "Sale record returned successfully",
                                                   "sale")
                    return jsonify({"error": "You didn't make this sale"}), 403
            else:
                return jsonify({
                    "error": "Please login to view this sale record"
                    }), 401
        # run if request is for all sale records and if it's a store
        # owner
        if "store_owner" in session:
            return jsonify({
                "message": "Sale records returned successfully",
                "sales": [sale_record.__dict__ for sale_record in sale_records]
            })
        return jsonify({"error": "Please login as a store owner"}), 401


# Map urls to view classes
app.add_url_rule('/api/v1/store-owner/register',
                 view_func=AppAuthView.as_view('store_owner_register'))
app.add_url_rule('/api/v1/store-owner/login',
                 view_func=AppAuthView.as_view('store_owner_login'))
app.add_url_rule('/api/v1/store-owner/attendant/register',
                 view_func=AppAuthView.as_view('store_attendant_register'))
app.add_url_rule('/api/v1/store-attendant/login',
                 view_func=AppAuthView.as_view('store_attendant_login'))
app.add_url_rule('/api/v1/products',
                 view_func=ProductView.as_view('product_view'),
                 methods=["GET", "POST"])
app.add_url_rule('/api/v1/products/<product_id>',
                 view_func=ProductView.as_view('product_view1'),
                 methods=["GET"])
app.add_url_rule('/api/v1/sales',
                 view_func=SaleView.as_view('sale_view'),
                 methods=["GET","POST"])
app.add_url_rule('/api/v1/sales/<sale_id>',
                 view_func=SaleView.as_view('sale_view1'), methods=["GET"])
