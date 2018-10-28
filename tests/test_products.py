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
        self.db_conn = DB()
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
            "unit_cost": 10000,
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

    def test_create_product_with_valid_fields(self):
        """
        Test to create product with valid fields
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        res = self.app.post("/api/v2/products",
                            headers=self.headers,
                            data=json.dumps(self.product))
        res_data = json.loads(res.data)
        expected_output = {
            "message": "Product created successfully",
        }
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res_data, expected_output)

    def test_create_product_with_missing_fields(self):
        """
        Test to create product with missing fields
        """
        self.product["name"] = ""
        self.headers["Authorization"] = "Bearer " + self.access_token
        res = self.app.post("/api/v2/products",
                            headers=self.headers,
                            data=json.dumps(self.product))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Product name, unit_cost and quantity is required"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)

    def test_create_product_with_invalid_data(self):
        """
        Test to create product with invalid data
        """
        self.product["unit_cost"] = "zjsvgjs"
        self.headers["Authorization"] = "Bearer " + self.access_token
        res = self.app.post("/api/v2/products",
                            headers=self.headers,
                            data=json.dumps(self.product))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Product unit_cost and quantity must be integers"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)

    def test_create_product_with_unauthenticated_user(self):
        """
        Test to create a without logging in as store owner
        """
        res = self.app.post("/api/v2/products",
                            headers=self.headers,
                            data=json.dumps(self.product))
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_create_product_as_store_attendant(self):
        """
        Test to create product as a store attendant
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers,
                      data=json.dumps(self.reg_data))
        res = self.app.post("/api/v2/auth/login",
                      headers=self.headers,
                      data=json.dumps(self.login_data))
        self.headers["Authorization"] = "Bearer " + json.loads(res.data)["token"]
        res = self.app.post("/api/v2/products",
                            headers=self.headers,
                            data=json.dumps(self.product))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Please login as a store owner"
        }
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res_data, expected_output)

    def test_get_all_products_authenticated_user(self):
        """
        Test getting all products as a logged in user
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/products",
                      headers=self.headers,
                      data=json.dumps(self.product))
        res = self.app.get("/api/v2/products",
                           headers=self.headers)
        res_data = json.loads(res.data)
        exepected_output = {
            "message": "Products returned successfully"
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data, exepected_output)

    def test_get_products_unauthenticated_user(self):
        """
        Test get products for unauthenticated user
        """
        res = self.app.get("/api/v2/products")
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_get_single_product_authenticated(self):
        """
        Test getting single product when logged in
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/products",
                      headers=self.headers,
                      data=json.dumps(self.product))
        product_id = self.db_conn.get_products()[0]["id"]
        res = self.app.get("/api/v2/products/" + str(product_id),
                           headers=self.headers)
        res_data = json.loads(res.data)
        exepected_output = {
            "message": "Product returned successfully"
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data, exepected_output)

    def test_get_product_unauthenticated_user(self):
        """
        Test get product for unauthenticated user
        """
        res = self.app.get("/api/v2/products/1")
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_get_product_not_exists(self):
        """
        Test get product which doesn't exists
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        res = self.app.get("/api/v2/products/1",
                           headers=self.headers)
        res_data = json.loads(res.data)
        expected_output = {
            "error": "This product does not exist"
        }
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data, expected_output)
    
    def test_modify_product_as_store_owner(self):
        """
        Test modify a product with valid data
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/products",
                      headers=self.headers,
                      data=json.dumps(self.product))
        product_id = self.db_conn.get_products()[0]["id"]
        self.product["name"] = "svdkjsd"
        res = self.app.put("/api/v2/products/" + str(product_id),
                           headers=self.headers,
                           data=json.dumps(self.product))
        res_data = json.loads(res.data)
        exepected_output = {
            "message": "Product updated successfully"
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data, exepected_output)
    
    def test_modify_product_as_store_attendant(self):
        """
        Test modify a product as store attendant
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/products",
                      headers=self.headers,
                      data=json.dumps(self.product))
        product_id = self.db_conn.get_products()[0]["id"]
        self.product["name"] = "svdkjsd"
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers,
                      data=json.dumps(self.reg_data))
        res = self.app.post("/api/v2/auth/login",
                      headers=self.headers,
                      data=json.dumps(self.login_data))
        self.headers["Authorization"] = "Bearer " + json.loads(res.data)["token"]
        res = self.app.put("/api/v2/products/" + str(product_id),
                           headers=self.headers,
                           data=json.dumps(self.product))
        res_data = json.loads(res.data)
        exepected_output = {
            "error": "Please login as a store owner"
        }
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res_data, exepected_output)
    
    def test_modify_product_non_existant(self):
        """
        Test modify a product which doesn't exist
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/products",
                      headers=self.headers,
                      data=json.dumps(self.product))
        self.product["name"] = "svdkjsd"
        res = self.app.put("/api/v2/products/553445354665789",
                           headers=self.headers,
                           data=json.dumps(self.product))
        res_data = json.loads(res.data)
        exepected_output = {
            "error": "The product you're trying to modify doesn't exist"
        }
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data, exepected_output)

    def test_modify_product_with_invalid_data(self):
        """
        Test modify a product with invalid data
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/products",
                      headers=self.headers,
                      data=json.dumps(self.product))
        product_id = self.db_conn.get_products()[0]["id"]
        self.product["unit_cost"] = "ksjdg"
        res = self.app.put("/api/v2/products/" + str(product_id),
                           headers=self.headers,
                           data=json.dumps(self.product))
        res_data = json.loads(res.data)
        exepected_output = {
            "error": "Product unit_cost and quantity must be integers"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, exepected_output)
    
    def test_modify_product_with_empty_value(self):
        """
        Test modify a product with empty value
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/products",
                      headers=self.headers,
                      data=json.dumps(self.product))
        product_id = self.db_conn.get_products()[0]["id"]
        self.product["unit_cost"] = ""
        res = self.app.put("/api/v2/products/" + str(product_id),
                           headers=self.headers,
                           data=json.dumps(self.product))
        res_data = json.loads(res.data)
        exepected_output = {
            "error": "Product name, unit_cost and quantity is required"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, exepected_output)
