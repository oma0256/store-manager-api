"""
File to test product view
"""

import unittest
import json
from api import views
from api.__init__ import app


class TestSaleView(unittest.TestCase):
    """
    Class to test sale view
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
        self.product = {
            "name": "Belt",
            "price": 10000,
            "quantity": 1,
            "category": "clothing"
        }
        self.sale = {
            "products": [self.product]
        }

    def tearDown(self):
        views.products = []
        views.store_attendants = []
        views.store_owners = []
        views.sale_records = []

    def test_create_sale_record_as_unauthenticated(self):
        """
        Test creating sale as store owner
        """
        res = self.app.post("/api/v1/sales",
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(self.sale))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Please login as a store attendant"
        }
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data, expected_output)

    def test_create_sale_with_missing_fields(self):
        """
        Test creating sale with missing fields
        """
        self.app.post("/api/v1/store-owner/attendant/register",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.reg_data))
        self.app.post("/api/v1/store-attendant/login",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.login_data))
        self.product["name"] = ""
        self.sale["products"] = [self.product]
        res = self.app.post("/api/v1/sales",
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(self.sale))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Product name is required"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)

    # def test_create_sale_with_invalid_data(self):
    #     """
    #     Test creating sale with invalid data
    #     """
    #     self.app.post("/api/v1/store-owner/attendant/register",
    #                   headers={"Content-Type": "application/json"},
    #                   data=json.dumps(self.reg_data))
    #     self.app.post("/api/v1/store-attendant/login",
    #                   headers={"Content-Type": "application/json"},
    #                   data=json.dumps(self.login_data))
    #     self.product["price"] = "bjzb"
    #     self.sale["products"] = [self.product]
    #     res = self.app.post("/api/v1/sales",
    #                         headers={"Content-Type": "application/json"},
    #                         data=json.dumps(self.sale))
    #     res_data = json.loads(res.data)
    #     expected_output = {
    #         "error": "Product price is invalid please an integer"
    #     }
    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(res_data, expected_output)

    def test_create_sale_with_valid_data(self):
        """
        Test creating sale with valid data
        """
        self.app.post("/api/v1/store-owner/attendant/register",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.reg_data))
        self.app.post("/api/v1/store-attendant/login",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.login_data))
        res = self.app.post("/api/v1/sales",
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(self.sale))
        res_data = json.loads(res.data)
        expected_output = {
            "message": "Sale created successfully",
            "sale": {
                "sale_id": 1,
                "products": [self.product],
                "attendant_name": "joe doe",
                "attendant_email": "joe@email.com",
                "total": 10000
            }
        }
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res_data, expected_output)

    def test_create_sale_as_store_owner(self):
        """
        Test creating sale as store owner
        """
        self.app.post("/api/v1/store-owner/register",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.reg_data))
        self.app.post("/api/v1/store-owner/login",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.login_data))
        res = self.app.post("/api/v1/sales",
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(self.sale))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Please login as a store attendant"
        }
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res_data, expected_output)

    def test_get_all_sale_records_authenticated_as_store_owner(self):
        """
        Test getting all sale records logged in as store owner
        """
        self.app.post("/api/v1/store-owner/register",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.reg_data))
        self.app.post("/api/v1/store-owner/login",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.login_data))
        self.app.post("/api/v1/store-owner/attendant/register",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.reg_data))
        self.app.post("/api/v1/store-attendant/login",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.login_data))
        self.app.post("/api/v1/sales",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.sale))
        res = self.app.get("/api/v1/sales")
        res_data = json.loads(res.data)
        exepected_output = {
            "message": "Sale records returned successfully",
            "sales": [{
                "sale_id": 1,
                "products": [self.product],
                "attendant_name": "joe doe",
                "attendant_email": "joe@email.com",
                "total": 10000
            }]
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data, exepected_output)

    def test_get_all_sale_records_unauthenticated_as_store_owner(self):
        """
        Test getting all sale records logged in as store owner
        """
        res = self.app.get("/api/v1/sales")
        res_data = json.loads(res.data)
        exepected_output = {
            "error": "Please login as a store owner"
        }
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data, exepected_output)

    def test_get_sale_record_as_store_owner(self):
        """
        Test getting a sale record as a store owner
        """
        self.app.post("/api/v1/store-owner/register",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.reg_data))
        self.app.post("/api/v1/store-owner/login",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.login_data))
        self.app.post("/api/v1/store-owner/attendant/register",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.reg_data))
        self.app.post("/api/v1/store-attendant/login",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.login_data))
        self.app.post("/api/v1/sales",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.sale))
        res = self.app.get("/api/v1/sales/1")
        res_data = json.loads(res.data)
        expected_output = {
            "message": "Sale record returned successfully",
            "sale": {
                "sale_id": 1,
                "products": [self.product],
                "attendant_name": "joe doe",
                "attendant_email": "joe@email.com",
                "total": 10000
            }
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data, expected_output)

    def test_get_sale_record_as_store_attendant(self):
        """
        Test getting a sale record as a store attendant if made it
        """
        self.app.post("/api/v1/store-owner/register",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.reg_data))
        self.app.post("/api/v1/store-owner/login",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.login_data))
        self.app.post("/api/v1/store-owner/attendant/register",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.reg_data))
        self.app.post("/api/v1/store-attendant/login",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.login_data))
        self.app.post("/api/v1/sales",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.sale))
        res = self.app.get("/api/v1/sales/1")
        res_data = json.loads(res.data)
        expected_output = {
            "message": "Sale record returned successfully",
            "sale": {
                "sale_id": 1,
                "products": [self.product],
                "attendant_name": "joe doe",
                "attendant_email": "joe@email.com",
                "total": 10000
            }
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data, expected_output)

    def test_get_sale_record_as_unauthenticated_user(self):
        """
        Test getting a sale record as unauthenticated user
        """
        res = self.app.get("/api/v1/sales/1")
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Please login to view this sale record"
        }
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data, expected_output)

    def test_get_sale_record_that_does_not_exist(self):
        """
        Test getting a sale record that doesn't exist
        """
        self.app.post("/api/v1/store-owner/register",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.reg_data))
        self.app.post("/api/v1/store-owner/login",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.login_data))
        self.app.post("/api/v1/store-owner/attendant/register",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.reg_data))
        self.app.post("/api/v1/store-attendant/login",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.login_data))
        res = self.app.get("/api/v1/sales/1")
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Sale record with this id doesn't exist"
        }
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data, expected_output)
