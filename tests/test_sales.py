"""
File to test product view
"""

import unittest
import json
from api.__init__ import app
from db import DB


class TestSaleView(unittest.TestCase):
    """
    Class to test sale view
    """
    
    def setUp(self):
        self.app = app.test_client()
        self.db_conn = DB()
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
        self.sale = {
            "product_id": 1,
            "quantity": 1
        }
        self.headers = {"Content-Type": "application/json"}
        response = self.app.post("/api/v2/auth/login",
                                  headers=self.headers,
                                  data=json.dumps(self.admin_login))
        self.access_token = json.loads(response.data)["token"]

    def tearDown(self):
        self.db_conn.drop_tables()

    def test_create_sale_record_as_unauthenticated(self):
        """
        Test creating sale as unauthenticated
        """
        res = self.app.post("/api/v2/sales",
                            headers=self.headers,
                            data=json.dumps(self.sale))
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_create_sale_with_missing_fields(self):
        """
        Test creating sale with missing fields
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        res = self.app.post("/api/v2/products",
                            headers=self.headers,
                            data=json.dumps(self.product))
        product_id = self.db_conn.get_products()[0]["id"]
        self.sale["product_id"] = ""
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers,
                      data=json.dumps(self.reg_data))
        res = self.app.post("/api/v2/auth/login",
                            headers=self.headers,
                            data=json.dumps(self.login_data))
        self.headers["Authorization"] = "Bearer " + json.loads(res.data)["token"]
        res = self.app.post("/api/v2/sales",
                            headers=self.headers,
                            data=json.dumps(self.sale))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Product id and quantity is required"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)

    def test_create_sale_with_valid_data(self):
        """
        Test creating sale with valid data
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        res = self.app.post("/api/v2/products",
                      headers=self.headers,
                      data=json.dumps(self.product))
        product_id = self.db_conn.get_products()[0]["id"]
        self.sale["product_id"] = product_id
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers,
                      data=json.dumps(self.reg_data))
        res = self.app.post("/api/v2/auth/login",
                            headers=self.headers,
                            data=json.dumps(self.login_data))
        self.headers["Authorization"] = "Bearer " + json.loads(res.data)["token"]
        res = self.app.post("/api/v2/sales",
                            headers=self.headers,
                            data=json.dumps(self.sale))
        res_data = json.loads(res.data)
        expected_output = {
            "message": "Sale made successfully"
        }
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res_data, expected_output)

    def test_create_sale_as_store_owner(self):
        """
        Test creating sale as store owner
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        res = self.app.post("/api/v2/products",
                      headers=self.headers,
                      data=json.dumps(self.product))
        product_id = self.db_conn.get_products()[0]["id"]
        self.sale["product_id"] = product_id
        res = self.app.post("/api/v2/sales",
                            headers=self.headers,
                            data=json.dumps(self.sale))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Please login as a store attendant"
        }
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res_data, expected_output)

    def test_create_sale_non_existant_product(self):
        """
        Test creating sale non existant product
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        res = self.app.post("/api/v2/products",
                      headers=self.headers,
                      data=json.dumps(self.product))
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers,
                      data=json.dumps(self.reg_data))
        res = self.app.post("/api/v2/auth/login",
                            headers=self.headers,
                            data=json.dumps(self.login_data))
        self.headers["Authorization"] = "Bearer " + json.loads(res.data)["token"]
        self.sale["product_id"] = 32435678908
        res = self.app.post("/api/v2/sales",
                            headers=self.headers,
                            data=json.dumps(self.sale))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "This product doesn't exist"
        }
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data, expected_output)

    def test_get_all_sale_records_authenticated_as_store_owner(self):
        """
        Test getting all sale records logged in as store owner
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        res = self.app.post("/api/v2/products",
                      headers=self.headers,
                      data=json.dumps(self.product))
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers,
                      data=json.dumps(self.reg_data))
        res = self.app.post("/api/v2/auth/login",
                            headers=self.headers,
                            data=json.dumps(self.login_data))
        self.headers["Authorization"] = "Bearer " + json.loads(res.data)["token"]
        self.app.post("/api/v2/sales",
                      headers=self.headers,
                      data=json.dumps(self.sale))
        response = self.app.post("/api/v2/auth/login",
                                  headers=self.headers,
                                  data=json.dumps(self.admin_login))
        self.access_token = json.loads(response.data)["token"]
        self.headers["Authorization"] = "Bearer " + self.access_token
        res = self.app.get("/api/v2/sales",
                           headers=self.headers)
        res_data = json.loads(res.data)
        exepected_output = {
            "message": "Sale records returned successfully",
            "sale_records": self.db_conn.get_sale_records()
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data, exepected_output)

    def test_get_sale_records_as_store_attendant(self):
        """
        Test getting a sale records as a store attendant if made it
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/products",
                      headers=self.headers,
                      data=json.dumps(self.product))
        product_id = self.db_conn.get_products()[0]["id"]
        self.sale["product_id"] = product_id
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers,
                      data=json.dumps(self.reg_data))
        res = self.app.post("/api/v2/auth/login",
                            headers=self.headers,
                            data=json.dumps(self.login_data))
        self.headers["Authorization"] = "Bearer " + json.loads(res.data)["token"]
        res = self.app.post("/api/v2/sales",
                            headers=self.headers,
                            data=json.dumps(self.sale))
        sale_record = self.db_conn.get_sale_records()[0]
        attendant_id = sale_record["attendant_id"]
        res = self.app.get("/api/v2/sales",
                           headers=self.headers)
        res_data = json.loads(res.data)
        expected_output = {
            "message": "Sale records returned successfully",
            "sale_records": self.db_conn.get_sale_records_user(attendant_id)
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data, expected_output)

    def test_get_all_sale_records_unauthenticated_user(self):
        """
        Test getting all sale records logged in as store owner
        """
        res = self.app.get("/api/v2/sales")
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_get_sale_record_as_store_owner(self):
        """
        Test getting a sale record as a store owner
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/products",
                      headers=self.headers,
                      data=json.dumps(self.product))
        product_id = self.db_conn.get_products()[0]["id"]
        self.sale["product_id"] = product_id
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers,
                      data=json.dumps(self.reg_data))
        res = self.app.post("/api/v2/auth/login",
                            headers=self.headers,
                            data=json.dumps(self.login_data))
        self.headers["Authorization"] = "Bearer " + json.loads(res.data)["token"]
        res = self.app.post("/api/v2/sales",
                            headers=self.headers,
                            data=json.dumps(self.sale))
        sale_record = self.db_conn.get_sale_records()[0]
        sale_id = sale_record["id"]
        response = self.app.post("/api/v2/auth/login",
                                  headers=self.headers,
                                  data=json.dumps(self.admin_login))
        self.access_token = json.loads(response.data)["token"]
        self.headers["Authorization"] = "Bearer " + self.access_token
        res = self.app.get("/api/v2/sales/" + str(sale_id),
                           headers=self.headers)
        res_data = json.loads(res.data)
        expected_output = {
            "message": "Sale record returned successfully",
            "sale_record": sale_record
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data, expected_output)

    def test_get_sale_record_as_store_attendant(self):
        """
        Test getting a sale record as a store attendant if made it
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/products",
                      headers=self.headers,
                      data=json.dumps(self.product))
        product_id = self.db_conn.get_products()[0]["id"]
        self.sale["product_id"] = product_id
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers,
                      data=json.dumps(self.reg_data))
        res = self.app.post("/api/v2/auth/login",
                            headers=self.headers,
                            data=json.dumps(self.login_data))
        self.headers["Authorization"] = "Bearer " + json.loads(res.data)["token"]
        res = self.app.post("/api/v2/sales",
                            headers=self.headers,
                            data=json.dumps(self.sale))
        sale_record = self.db_conn.get_sale_records()[0]
        sale_id = sale_record["id"]
        res = self.app.get("/api/v2/sales/" + str(sale_id),
                           headers=self.headers)
        res_data = json.loads(res.data)
        expected_output = {
            "message": "Sale record returned successfully",
            "sale_record": sale_record
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data, expected_output)

    def test_get_sale_record_that_does_not_exist(self):
        """
        Test getting a sale record that doesn't exist
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        res = self.app.get("/api/v2/sales/1",
                           headers=self.headers)
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Sale record with this id doesn't exist"
        }
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data, expected_output)