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

    def tearDown(self):
        self.db_conn.drop_tables()

    
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
            "error": "First name and last name are required and must be alphabets"
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
            "error": "Passwords are required and must match"
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
            "error": "Please use a valid email address"
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
        self.db_conn = DB()
        self.app = app.test_client()
        self.login_data = {
            "email": "admin@email.com",
            "password": "pass1234"
        }

    def tearDown(self):
        self.db_conn.drop_tables()
    
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
        self.assertEqual(res.status_code, 400)
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
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)


class TestToggleRights(unittest.TestCase):
    def setUp(self):
        self.db_conn = DB()
        self.app = app.test_client()
        self.admin_login = {
            "email": "admin@email.com",
            "password": "pass1234"
        }
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
        self.headers = {"Content-Type": "application/json"}
        response = self.app.post("/api/v2/auth/login",
                                  headers=self.headers,
                                  data=json.dumps(self.admin_login))
        self.admin_token = json.loads(response.data)["token"]
        self.headers["Authorization"] = "Bearer " + self.admin_token
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers,
                      data=json.dumps(self.reg_data))
        response = self.app.post("/api/v2/auth/login",
                                  headers=self.headers,
                                  data=json.dumps(self.login_data))
        self.attendant_token = json.loads(response.data)["token"]

    def tearDown(self):
        self.db_conn.drop_tables()
    
    def test_toggle_rights_as_store_attendant(self):
        self.headers["Authorization"] = "Bearer " + self.attendant_token
        res = self.app.get("/api/v2/user/2/toggle-rights",
                           headers=self.headers)
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Please login as the store owner"
        }
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res_data, expected_output)
    
    def test_toggle_rights_unauthorized(self):
        res = self.app.get("/api/v2/user/2/toggle-rights")
        self.assertEqual(res.status_code, 401)
    
    def test_toggle_rights_of_admin(self):
        res = self.app.get("/api/v2/user/1/toggle-rights",
                           headers=self.headers)
        res_data = json.loads(res.data)
        expected_output = {
            "error": "You can't change store owner's rights"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)
    
    def test_toggle_rights_of_non_existant_user(self):
        res = self.app.get("/api/v2/user/1264525349652352/toggle-rights",
                           headers=self.headers)
        res_data = json.loads(res.data)
        expected_output = {
            "error": "User with this id doesn't exist"
        }
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data, expected_output)
    
    def test_toggle_rights_of_store_attendant(self):
        user_id = self.db_conn.get_users()[-1]["id"]
        res = self.app.get(f"/api/v2/user/{user_id}/toggle-rights",
                           headers=self.headers)
        res_data = json.loads(res.data)
        expected_output = {
            "message": "Assigned admin rights"
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data, expected_output)
        res = self.app.get(f"/api/v2/user/{user_id}/toggle-rights",
                           headers=self.headers)
        res_data = json.loads(res.data)
        expected_output["message"] = "Admin rights revoked"
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data, expected_output)
