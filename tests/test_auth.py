"""
File to test authentication for the application
"""
import unittest
import json
from api.__init__ import app
from db import DB


class TestSoreAttendantauth(unittest.TestCase):
    """
    Test store attendant authentication
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
        self.headers = {"Content-Type": "application/json"}
        response = self.app.post("/api/v2/auth/login",
                                  headers=self.headers,
                                  data=json.dumps(self.admin_login))
        self.access_token = json.loads(response.data)["token"]

    
    def test_register_with_unathenticated_user(self):
        """
        Test registration with unathenticated user
        """
        res = self.app.post("/api/v2/auth/signup",
                            headers=self.headers,
                            data=json.dumps(self.reg_data))
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertIsNone(res_data.get("token"))

    def test_register_invalid_email(self):
        """
        Test registration with invalid email
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.reg_data["email"] = "ashga"
        res = self.app.post("/api/v2/auth/signup",
                            headers=self.headers,
                            data=json.dumps(self.reg_data))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Please use a valid email address"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)

    def test_register_invalid_first_name(self):
        """
        Test registration with invalid first name
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.reg_data["first_name"] = "sbfsb4124324"
        res = self.app.post("/api/v2/auth/signup",
                            headers=self.headers,
                            data=json.dumps(self.reg_data))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "First and last name should only be alphabets"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)

    def test_register_with_unmatching_password(self):
        """
        Test registration with unmatching passwords
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.reg_data["password"] = "123"
        res = self.app.post("/api/v2/auth/signup",
                            headers=self.headers,
                            data=json.dumps(self.reg_data))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Passwords must match"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)

    def test_register_missing_fields(self):
        """
        Test registration with missing fields
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.reg_data["email"] = ""
        res = self.app.post("/api/v2/auth/signup",
                            headers=self.headers,
                            data=json.dumps(self.reg_data))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "First name, last name, email, password and confirm password fields are required"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)

    def test_register_duplicate_user(self):
        """
        Test register already registered store attendant
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers,
                      data=json.dumps(self.reg_data))
        res = self.app.post("/api/v2/auth/signup",
                            headers=self.headers,
                            data=json.dumps(self.reg_data))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "User with this email already exists"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)

    def test_register_using_store_attendant(self):
        """
        Test register as a store attendant
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers,
                      data=json.dumps(self.reg_data))
        auth_res = self.app.post("/api/v2/auth/login",
                                 headers=self.headers,
                                 data=json.dumps(self.login_data))
        self.headers["Authorization"] = "Bearer " + json.loads(auth_res.data)["token"]
        self.reg_data["email"] = "email@email.com"
        res = self.app.post("/api/v2/auth/signup",
                            headers=self.headers,
                            data=json.dumps(self.reg_data))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Please login as store owner to add store attendant"
        }
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res_data, expected_output)

    def test_register_using_unauthenticated_user(self):
        """
        Test register as unauthenticated user
        """
        res = self.app.post("/api/v2/auth/signup",
                            headers=self.headers,
                            data=json.dumps(self.reg_data))
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_login_valid_data(self):
        """
        Test login with valid data
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers,
                      data=json.dumps(self.reg_data))
        res = self.app.post("/api/v2/auth/login",
                            headers=self.headers,
                            data=json.dumps(self.login_data))
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res_data["token"])


class TestStoreOwnerAuth(unittest.TestCase):
    """
    Test store owner authentication
    """

    def setUp(self):
        self.app = app.test_client()
        self.login_data = {
            "email": "admin@email.com",
            "password": "pass1234"
        }
    
    def test_login_valid_data(self):
        """
        Test login with valid data
        """
        res = self.app.post("/api/v2/auth/login",
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(self.login_data))
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertIsNotNone(res_data["token"])

    def test_login_with_missing_fields(self):
        """
        Test login with some missing fields
        """
        self.login_data["password"] = ""
        res = self.app.post("/api/v2/auth/login",
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(self.login_data))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Email and password is required"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)

    def test_login_invalid_password(self):
        """
        Test login with invalid password
        """
        self.login_data["password"] = "kjsdvjj"
        res = self.app.post("/api/v2/auth/login",
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(self.login_data))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Invalid email or password"
        }
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data, expected_output)

    def test_login_unregistered_store_owner(self):
        """
        Test login with unregistered user
        """
        self.login_data["email"] = "admin1234@email.com"
        res = self.app.post("/api/v2/auth/login",
                            headers={"Content-Type": "application/json"},
                            data=json.dumps(self.login_data))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Please register to login"
        }
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data, expected_output)
