"""
File to handle application views
"""
from functools import partial
from flask import jsonify, request, session
from flask.views import MethodView
from api.models import Product, Sale
from api.__init__ import app
from api.utils.decorators import (is_store_owner_attendant,
                                  is_store_owner_or_attendant,
                                  is_forbidden)
from api.utils.auth_functions import register_user, login_user
from api.utils.validators import validate_product
from api.utils.generate_id import create_id

store_owner_decorator = partial(is_store_owner_attendant,
                                user="store_owner",
                                error_msg="Please login as a store owner")
store_attendant_decorator = partial(is_store_owner_attendant,
                                    user="store_attendant",
                                    error_msg="Please login as a store attendant")
not_store_owner = partial(is_forbidden,
                          user="store_attendant",
                          error_msg="Please login as a store owner")
not_store_attendant = partial(is_forbidden,
                              user="store_owner",
                              error_msg="Please login as a store attendant")

# Holds store owners
store_owners = []
# Hold store attendants
store_attendants = []
# Store products
products = []
# Store sales
sale_records = []


@app.route("/")
def home_page():
    return "Welcome to the store manager"


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
    @not_store_owner
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
        res = validate_product(name, price, quantity)
        if res:
            return res

        product_id = create_id(products)
        # create a product object
        new_product = Product(product_id=product_id, name=name, price=price,
                              quantity=quantity, category=category)
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
            product = [pro for pro in products if pro.id == int(product_id)]
            # Check if product doesn't exist
            if not product:
                return jsonify({
                    "error": "This product does not exist"
                }), 404
            return jsonify({
                "message": "Product returned successfully",
                "products": product[0].__dict__
                })
        # Get all products
        return jsonify({
            "message": "Products returned successfully",
            "products": [product.__dict__ for product in products]
        })


class SaleView(MethodView):
    """
    Class to perform http methods on sales
    """
    @not_store_attendant
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
            # validate each product
            res = validate_product(name, price, quantity)
            if res:
                return res
            total += price
        sale_id = create_id(sale_records)
        store_attendant = [att for att in store_attendants if att.email == session["store_attendant"]]
        if store_attendant[0]:
            attendant_email = session["store_attendant"]
            sale = Sale(sale_id, cart_items, attendant_email, total)
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
            # Return a list of a specific sale record
            sale = [s for s in sale_records if s.id == int(sale_id)]
            # Check if sale doesn't exist
            if not sale:
                return jsonify({
                    "error": "Sale record with this id doesn't exist"
                }), 404
            # run if it's a store owner
            if "store_owner" in session:
                return jsonify({
                    "message": "Sale record returned successfully",
                    "sale": sale[0].__dict__
                    })
            # run if it's a store attendant
            elif "store_attendant" in session:
                if sale[0].attendant_email == session["store_attendant"]:
                    return jsonify({
                        "message": "Sale record returned successfully",
                        "sale": sale[0].__dict__
                        })
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
view = not_store_owner(store_owner_decorator(AppAuthView.as_view('store_attendant_register')))
app.add_url_rule('/api/v1/store-owner/register',
                 view_func=AppAuthView.as_view('store_owner_register'))
app.add_url_rule('/api/v1/store-owner/login',
                 view_func=AppAuthView.as_view('store_owner_login'))
app.add_url_rule('/api/v1/store-owner/attendant/register',
                 view_func=view)
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
