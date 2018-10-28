"""
File to test authentication for the application
"""
import unittest
import json
from api.__init__ import app


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


# class TestSoreAttendantauth(unittest.TestCase):
#     """
#     Test store attendant authentication
#     """
#     def setUp(self):
#         self.app = app.test_client()
#         self.reg_data = {
#             "first_name": "joe",
#             "last_name": "doe",
#             "email": "joe@email.com",
#             "password": "pass1234",
#             "confirm_password": "pass1234"
#         }
#         self.login_data = {
#             "email": "joe@email.com",
#             "password": "pass1234"
#         }

#     def tearDown(self):
#         views.store_attendants = []

#     def test_register_valid_data(self):
#         """
#         Test registration with valid data
#         """
#         self.app.post("/api/v1/store-owner/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-owner/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         res = self.app.post("/api/v1/store-owner/attendant/register",
#                             headers={"Content-Type": "application/json"},
#                             data=json.dumps(self.reg_data))
#         res_data = json.loads(res.data)
#         expected_output = {
#             "message": "Store attendant successfully registered"
#         }
#         self.assertEqual(res.status_code, 201)
#         self.assertEqual(res_data, expected_output)

#     def test_register_invalid_email(self):
#         """
#         Test registration with valid data
#         """
#         self.app.post("/api/v1/store-owner/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-owner/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         self.reg_data["email"] = "ashga"
#         res = self.app.post("/api/v1/store-owner/attendant/register",
#                             headers={"Content-Type": "application/json"},
#                             data=json.dumps(self.reg_data))
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "Please use a valid email address"
#         }
#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(res_data, expected_output)

#     def test_register_invalid_first_name(self):
#         """
#         Test registration with valid data
#         """
#         self.app.post("/api/v1/store-owner/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-owner/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         self.reg_data["first_name"] = "4124324"
#         res = self.app.post("/api/v1/store-owner/attendant/register",
#                             headers={"Content-Type": "application/json"},
#                             data=json.dumps(self.reg_data))
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "First and last name should only be alphabets"
#         }
#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(res_data, expected_output)

#     def test_register_with_short_password(self):
#         """
#         Test registration with valid data
#         """
#         self.app.post("/api/v1/store-owner/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-owner/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         self.reg_data["password"] = "123"
#         res = self.app.post("/api/v1/store-owner/attendant/register",
#                             headers={"Content-Type": "application/json"},
#                             data=json.dumps(self.reg_data))
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "Password should be more than 5 characters"
#         }
#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(res_data, expected_output)

#     def test_register_missing_fields(self):
#         """
#         Test registration with missing fields
#         """
#         self.app.post("/api/v1/store-owner/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-owner/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         self.reg_data["email"] = ""
#         res = self.app.post("/api/v1/store-owner/attendant/register",
#                             headers={"Content-Type": "application/json"},
#                             data=json.dumps(self.reg_data))
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "First name, last name, email and password field is required"
#         }
#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(res_data, expected_output)

#     def test_register_duplicate_user(self):
#         """
#         Test register already registered store attendant
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
#         res = self.app.post("/api/v1/store-owner/attendant/register",
#                             headers={"Content-Type": "application/json"},
#                             data=json.dumps(self.reg_data))
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "User with this email address already exists"
#         }
#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(res_data, expected_output)

#     def test_register_using_store_attendant(self):
#         """
#         Test register as a store attendant
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
#         res = self.app.post("/api/v1/store-owner/attendant/register",
#                             headers={"Content-Type": "application/json"},
#                             data=json.dumps(self.reg_data))
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "Please login as a store owner"
#         }
#         self.assertEqual(res.status_code, 403)
#         self.assertEqual(res_data, expected_output)

#     def test_register_using_unauthenticated_user(self):
#         """
#         Test register as unauthenticated user
#         """
#         res = self.app.post("/api/v1/store-owner/attendant/register",
#                             headers={"Content-Type": "application/json"},
#                             data=json.dumps(self.reg_data))
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "Please login as a store owner"
#         }
#         self.assertEqual(res.status_code, 401)
#         self.assertEqual(res_data, expected_output)

#     def test_login_valid_data(self):
#         """
#         Test login with valid data
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
#         res = self.app.post("/api/v1/store-attendant/login",
#                             headers={"Content-Type": "application/json"},
#                             data=json.dumps(self.login_data))
#         res_data = json.loads(res.data)
#         expected_output = {
#             "message": "Store attendant logged in successfully"
#         }
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res_data, expected_output)

#     def test_login_with_missing_fields(self):
#         """
#         Test login with some missing fields
#         """
#         self.app.post("/api/v1/store-owner/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-owner/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         self.login_data["password"] = ""
#         self.app.post("/api/v1/store-owner/attendant/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         res = self.app.post("/api/v1/store-attendant/login",
#                             headers={"Content-Type": "application/json"},
#                             data=json.dumps(self.login_data))
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "Email and password is required"
#         }
#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(res_data, expected_output)

#     def test_login_invalid_password(self):
#         """
#         Test login with invalid password
#         """
#         self.app.post("/api/v1/store-owner/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-owner/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         self.login_data["password"] = "kjsdvjj"
#         self.app.post("/api/v1/store-owner/attendant/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         res = self.app.post("/api/v1/store-attendant/login",
#                             headers={"Content-Type": "application/json"},
#                             data=json.dumps(self.login_data))
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "Invalid email or password"
#         }
#         self.assertEqual(res.status_code, 401)
#         self.assertEqual(res_data, expected_output)

#     def test_login_unregistered_store_owner(self):
#         """
#         Test login with unregistered user
#         """
#         self.app.post("/api/v1/store-owner/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-owner/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         res = self.app.post("/api/v1/store-attendant/login",
#                             headers={"Content-Type": "application/json"},
#                             data=json.dumps(self.login_data))
#         res_data = json.loads(res.data)
#         expected_output = {
#             "error": "Please register to login"
#         }
#         self.assertEqual(res.status_code, 401)
#         self.assertEqual(res_data, expected_output)
