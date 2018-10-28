"""
File to test product view
"""

import unittest
import json
from api import views
from api.__init__ import app
from db import DB


app.config['TESTING'] = True
class TestProductView(unittest.TestCase):
    """
    Class to test product view
    """
    def setUp(self):
        self.app = app.test_client()
        self.reg_data = {
            "first_name": "joe",
            "last_name": "doe",
            "email": "joe@email.com",
            "password": "pass1234",
            "confirm_password": "pass1234"
        }
        self.login_data = {
            "email": "joe@email.com",
            "password": "pass1234"
        }
        self.admin_login = {
            "email": "admin@email.com",
            "password": "pass1234"
        }
        self.product = {
            "name": "Belt",
            "price": 10000,
            "quantity": 3
        }
        self.headers = {"Content-Type": "application/json"}
        response = self.app.post("/api/v2/auth/login",
                                  headers=self.headers,
                                  data=json.dumps(self.admin_login))
        self.access_token = json.loads(response.data)["token"]

    def tearDown(self):
        db_conn = DB()
        db_conn.delete_products()
        db_conn.delete_attendants()

#     def test_create_product_with_valid_fields(self):
#         """
#         Test to create product with valid fields
#         """
#         self.app.post("/api/v1/store-owner/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-owner/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         res = self.app.post("/api/v1/products",
#                             headers={"Content-Type": "application/json"},
#                             data=json.dumps(self.product))
#         res_data = json.loads(res.data)
#         self.product["id"] = 1
#         expected_output = {
#             "message": "Product created successfully",
#             "product": self.product
#         }
#         self.assertEqual(res.status_code, 201)
#         self.assertEqual(res_data, expected_output)

#     def test_create_product_with_missing_fields(self):
#         """
#         Test to create product with missing fields
#         """
#         self.app.post("/api/v1/store-owner/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-owner/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         self.product["name"] = ""
#         res = self.app.post("/api/v1/products",
#                             headers={"Content-Type": "application/json"},
#                             data=json.dumps(self.product))
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "Product name, price and quantity is required"
#         }
#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(res_data, expected_output)

#     def test_create_product_with_invalid_data(self):
#         """
#         Test to create product with invalid data
#         """
#         self.app.post("/api/v1/store-owner/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-owner/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         self.product["price"] = "zjsvgjs"
#         res = self.app.post("/api/v1/products",
#                             headers={"Content-Type": "application/json"},
#                             data=json.dumps(self.product))
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "Product price and quantity must be integers"
#         }
#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(res_data, expected_output)

#     def test_create_product_with_unauthenticated_user(self):
#         """
#         Test to create a without logging in as store owner
#         """
#         res = self.app.post("/api/v1/products",
#                             headers={"Content-Type": "application/json"},
#                             data=json.dumps(self.product))
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "Please login as a store owner"
#         }
#         self.assertEqual(res.status_code, 401)
#         self.assertEqual(res_data, expected_output)

#     def test_create_product_as_store_attendant(self):
#         """
#         Test to create product as a store attendant
#         """
#         self.app.post("/api/v1/store-owner/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-owner/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         self.app.post("/api/v1/store-owner/attendant/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-attendant/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         res = self.app.post("/api/v1/products",
#                             headers={"Content-Type": "application/json"},
#                             data=json.dumps(self.product))
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "Please login as a store owner"
#         }
#         self.assertEqual(res.status_code, 403)
#         self.assertEqual(res_data, expected_output)

#     def test_get_all_products_authenticated_as_store_owner(self):
#         """
#         Test getting all products logged in as store owner
#         """
#         self.app.post("/api/v1/store-owner/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-owner/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         self.app.post("/api/v1/products",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.product))
#         res = self.app.get("/api/v1/products")
#         res_data = json.loads(res.data)
#         self.product["id"] = 1
#         exepected_output = {
#             "message": "Products returned successfully",
#             "products": [self.product]
#         }
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res_data, exepected_output)

#     def test_get_all_products_authenticated_as_store_attendant(self):
#         """
#         Test getting all products logged in as store attendant
#         """
#         self.app.post("/api/v1/store-owner/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-owner/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         self.app.post("/api/v1/products",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.product))
#         self.app.post("/api/v1/store-owner/attendant/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-attendant/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         res = self.app.get("/api/v1/products")
#         res_data = json.loads(res.data)
#         self.product["id"] = 1
#         exepected_output = {
#             "message": "Products returned successfully",
#             "products": [self.product]
#         }
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res_data, exepected_output)

#     def test_get_products_unauthenticated_user(self):
#         """
#         Test get products for unauthenticated user
#         """
#         res = self.app.get("/api/v1/products")
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "Please login as a store owner or attendant"
#         }
#         self.assertEqual(res.status_code, 401)
#         self.assertEqual(res_data, expected_output)

#     def test_get_single_product_authenticated_as_store_owner(self):
#         """
#         Test getting single product logged in as store owner
#         """
#         self.app.post("/api/v1/store-owner/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-owner/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         self.app.post("/api/v1/products",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.product))
#         res = self.app.get("/api/v1/products/1")
#         res_data = json.loads(res.data)
#         self.product["id"] = 1
#         exepected_output = {
#             "message": "Product returned successfully",
#             "products": self.product
#         }
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res_data, exepected_output)

#     def test_get_single_product_authenticated_as_store_attendant(self):
#         """
#         Test getting single products logged in as store attendant
#         """
#         self.app.post("/api/v1/store-owner/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-owner/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         self.app.post("/api/v1/products",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.product))
#         self.app.post("/api/v1/store-owner/attendant/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-attendant/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         res = self.app.get("/api/v1/products/1")
#         res_data = json.loads(res.data)
#         self.product["id"] = 1
#         exepected_output = {
#             "message": "Product returned successfully",
#             "products": self.product
#         }
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res_data, exepected_output)

#     def test_get_product_unauthenticated_user(self):
#         """
#         Test get product for unauthenticated user
#         """
#         res = self.app.get("/api/v1/products/1")
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "Please login as a store owner or attendant"
#         }
#         self.assertEqual(res.status_code, 401)
#         self.assertEqual(res_data, expected_output)

#     def test_get_product_not_exists(self):
#         """
#         Test get product which doesn't exists
#         """
#         self.app.post("/api/v1/store-owner/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-owner/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         res = self.app.get("/api/v1/products/1")
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "This product does not exist"
#         }
#         self.assertEqual(res.status_code, 404)
#         self.assertEqual(res_data, expected_output)
