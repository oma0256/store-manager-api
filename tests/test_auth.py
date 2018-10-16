"""
File to test authentication for the application
"""
import unittest
import json
from api.__init__ import app
from api import views


class TestStoreOwnerAuth(unittest.TestCase):
    """
    Test store owner authentication
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

    def tearDown(self):
        views.store_owners = []

    def test_register_valid_data(self):
        """
        Test registration with valid data
        """
        res = self.app.post("/api/v1/store-owner/register",
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(self.reg_data))
        res_data = json.loads(res.data)
        expected_output = {
            "message": "Store owner successfully registered"
        }
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res_data, expected_output)

    def test_register_missing_fields(self):
        """
        Test registration with missing fields
        """
        self.reg_data["email"] = ""
        res = self.app.post("/api/v1/store-owner/register",
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(self.reg_data))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Email field is required"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)

    def test_register_invalid_data(self):
        """
        Test registration with invalid email
        """
        self.reg_data["email"] = "okay"
        res = self.app.post("/api/v1/store-owner/register",
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(self.reg_data))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Please enter a valid email"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)

    def test_register_unmatched_passwords(self):
        """
        Test registration with unmatching password
        """
        self.reg_data["confirm_password"] = "okay"
        res = self.app.post("/api/v1/store-owner/register",
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(self.reg_data))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "The passwords must match"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)

    def test_register_duplicate_user(self):
        """
        Test register already registered store owner
        """
        self.app.post("/api/v1/store-owner/register",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.reg_data))
        res = self.app.post("/api/v1/store-owner/register",
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(self.reg_data))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "User with this email address already exists"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)

    def test_login_valid_data(self):
        self.app.post("/api/v1/store-owner/register",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.reg_data))
        res = self.app.post("/api/v1/store-owner/login",
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(self.login_data))
        res_data = json.loads(res.data)
        expected_output = {
            "message": "Store owner logged in successfully"
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data, expected_output)

    def test_login_with_missing_fields(self):
        self.login_data["password"] = ""
        self.app.post("/api/v1/store-owner/register",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(self.reg_data))
        res = self.app.post("/api/v1/store-owner/login",
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(self.login_data))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Password field is required"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)
