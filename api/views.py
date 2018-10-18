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

# Holds store owners
store_owners = []
# Hold store attendants
store_attendants = []
# Store products
products = []
# Store sales
sale_records = []


class StoreOwnerRegister(MethodView):
    """
    Class to register store owner
    """
    def post(self):
        """
        Method that registers store owner
        """
        # data being sent
        data = request.get_json()
        # funtion returns a json response and status code
        res = register_user(data, store_owners, True)
        return res


class StoreOwnerLogin(MethodView):
    """
    Class to login store owner
    """
    def post(self):
        """
        Method to perform login of store owner
        """
        # data being sent
        data = request.get_json()
        # funtion returns a json response and status code
        res = login_user(data, store_owners, True)
        return res


class StoreAttendantRegister(MethodView):
    """
    Class to register store attendant
    """
    def post(self):
        """
        Method that registers store attendant
        """
        # data being sent
        data = request.get_json()
        # funtion returns a json response and status code
        res = register_user(data, store_attendants, False)
        return res


class StoreAttendantLogin(MethodView):
    """
    Class to login store attendant
    """
    def post(self):
        """
        Method to perform login of store attendant
        """
        # data being sent
        data = request.get_json()
        # funtion returns a json response and status code
        res = login_user(data, store_attendants, False)
        return res


# class ProductView(MethodView):
#     """
#     Class to perform http methods on products
#     """
#     @is_not_store_owner
#     @is_store_owner
#     def post(self):
#         """
#         Handles creating of a product
#         """
#         data = request.get_json()
#         # Get the fields which were sent
#         name = data.get("name")
#         price = data.get("price")
#         quantity = data.get("quantity")
#         category = data.get("category")
#         # validates product and returns json response and status code
#         res = validate_product(name, price, quantity, category)
#         if res:
#             return res

#         product_id = len(products) + 1
#         # create a product object
#         new_product = Product(product_id, name, price, quantity, category)
#         # appends the product object to list
#         products.append(new_product)
#         return jsonify({
#             "message": "Product created successfully",
#             "product": new_product.__dict__
#             }), 201

#     @is_store_owner_or_attendant
#     def get(self, product_id=None):
#         """
#         Get all products
#         """
#         # Check if an id has been passed
#         if product_id:
#             for product in products:
#                 # Check if product exists
#                 if product.product_id == int(product_id):
#                     return jsonify({
#                         "message": "Product returned successfully",
#                         "products": product.__dict__
#                     })
#             return jsonify({"error": "This product does not exist"}), 404
#         return jsonify({
#             "message": "Products returned successfully",
#             "products": [product.__dict__ for product in products]
#         })


@is_not_store_owner
@is_store_owner
@app.route('/api/v1/products', methods=["POST"])
def create_product(self):
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
@app.route('/api/v1/products/<product_id>')
def get_products(self, product_id=None):
    """
    Get all products
    """
    # Check if an id has been passed
    if product_id:
        for product in products:
            # Check if product exists
            if product.product_id == int(product_id):
                return jsonify({
                    "message": "Product returned successfully",
                    "products": product.__dict__
                })
        return jsonify({"error": "This product does not exist"}), 404
    return jsonify({
        "message": "Products returned successfully",
        "products": [product.__dict__ for product in products]
    })


# class SaleView(MethodView):
#     """
#     Class to perform http methods on sales
#     """
#     @is_not_store_attendant
#     @is_store_attendant
#     def post(self):
#         """
#         Method to create a sale record
#         """
#         data = request.get_json()
#         # get items being sold
#         cart_items = data.get("products")
#         total = 0
#         for cart_item in cart_items:
#             name = cart_item.get("name")
#             price = cart_item.get("price")
#             quantity = cart_item.get("quantity")
#             category = cart_item.get("category")
#             # validate each product
#             res = validate_product(name, price, quantity, category)
#             if res:
#                 return res
#             total += price
#         sale_id = len(sale_records) + 1
#         attendant_name = ""
#         for store_attendant in store_attendants:
#             if store_attendant.email == session["store_attendant"]:
#                 attendant_name = store_attendant.first_name + " " + store_attendant.last_name
#                 attendant_email = session["store_attendant"]
#                 sale = Sale(sale_id, cart_items, attendant_name, attendant_email, total)
#                 sale_records.append(sale)
#                 return jsonify({
#                     "message": "Sale created successfully",
#                     "sale": sale.__dict__
#                 }), 201

#     def get(self, sale_id=None):
#         """
#         Perform GET on sale records
#         """
#         # run if request is for a single sale record
#         if sale_id:
#             # run if it's a store owner
#             if "store_owner" in session:
#                 for sale_record in sale_records:
#                     # check if sale record exists
#                     if sale_record.sale_id == int(sale_id):
#                         return jsonify({
#                             "message": "Sale record returned successfully",
#                             "sale": sale_record.__dict__
#                         })
#             # run if it's a store attendant
#             elif "store_attendant" in session:
#                 for sale_record in sale_records:
#                     # check if sale record exists
#                     if sale_record.sale_id == int(sale_id):
#                         # check if store attendant created the sale record
#                         if sale_record.attendant_email == session["store_attendant"]:
#                             return jsonify({
#                                 "message": "Sale record returned successfully",
#                                 "sale": sale_record.__dict__
#                             })
#                         return jsonify({
#                             "error": "You didn't make this sale"
#                         }), 403
#             else:
#                 return jsonify({
#                     "error": "Please login to view this sale record"
#                     }), 401
#             return jsonify({
#                 "error": "Sale record with this id doesn't exist"
#             }), 404
#         # run if request is for all sale records and if it's a store
#         # owner
#         if "store_owner" in session:
#             return jsonify({
#                 "message": "Sale records returned successfully",
#                 "sales": [sale_record.__dict__ for sale_record in sale_records]
#             })
#         return jsonify({"error": "Please login as a store owner"}), 401

@is_not_store_attendant
@is_store_attendant
@app.route('/api/v1/sales', methhods=["POST"])
def create_sale(self):
    """
    Method to create a sale record
    """
    data = request.get_json()
    # get items being sold
    cart_items = data.get("products")
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

@app.route('/api/v1/sales/<sale_id>')
def get_sales(self, sale_id=None):
    """
    Perform GET on sale records
    """
    # run if request is for a single sale record
    if sale_id:
        # run if it's a store owner
        if "store_owner" in session:
            for sale_record in sale_records:
                # check if sale record exists
                if sale_record.sale_id == int(sale_id):
                    return jsonify({
                        "message": "Sale record returned successfully",
                        "sale": sale_record.__dict__
                    })
        # run if it's a store attendant
        elif "store_attendant" in session:
            for sale_record in sale_records:
                # check if sale record exists
                if sale_record.sale_id == int(sale_id):
                    # check if store attendant created the sale record
                    if sale_record.attendant_email == session["store_attendant"]:
                        return jsonify({
                            "message": "Sale record returned successfully",
                            "sale": sale_record.__dict__
                        })
                    return jsonify({
                        "error": "You didn't make this sale"
                    }), 403
        else:
            return jsonify({
                "error": "Please login to view this sale record"
                }), 401
        return jsonify({
            "error": "Sale record with this id doesn't exist"
        }), 404
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
                 view_func=StoreOwnerRegister.as_view('store_owner_register'))
app.add_url_rule('/api/v1/store-owner/login',
                 view_func=StoreOwnerLogin.as_view('store_owner_login'))
app.add_url_rule('/api/v1/store-owner/attendant/register',
                 view_func=StoreAttendantRegister.as_view('store_attendant_register'))
app.add_url_rule('/api/v1/store-attendant/login',
                 view_func=StoreAttendantLogin.as_view('store_attendant_login'))
# app.add_url_rule('/api/v1/products',
#                  view_func=ProductView.as_view('product_view'), methods=["GET","POST"])
# app.add_url_rule('/api/v1/products/<product_id>',
#                  view_func=ProductView.as_view('product_view1'), methods=["GET"])
# app.add_url_rule('/api/v1/sales',
#                  view_func=SaleView.as_view('sale_view'), methods=["GET","POST"])
# app.add_url_rule('/api/v1/sales/<sale_id>',
#                  view_func=SaleView.as_view('sale_view1'), methods=["GET"])
