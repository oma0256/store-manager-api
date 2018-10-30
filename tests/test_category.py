import unittest
import json
from api import views
from api.__init__ import app
from db import DB


class TestProductView(unittest.TestCase):
    """
    Class to test product view
    """
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        self.app = app.test_client()
        self.admin_login = {
            "email": "admin@email.com",
            "password": "pass1234"
        }
        self.headers = {"Content-Type": "application/json"}
        response = self.app.post("/api/v2/auth/login",
                                  headers=self.headers,
                                  data=json.dumps(self.admin_login))
        self.access_token = json.loads(response.data)["token"]
        self.category = {
            "name": "Tech",
            "description": "This is tech"
        }

    def test_create_category_with_valid_data(self):
        self.headers["Authorization"] = "Bearer " + self.access_token
        res = self.app.post("/api/v2/categories",
                            headers=self.headers,
                            data=json.dumps(self.category))
        res_data = json.loads(res.data)
        expected_output = {
            "message": "Successfully created product category"
        }
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res_data, expected_output)

    def test_create_category_with_missing_fields(self):
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.category["name"] = ""
        res = self.app.post("/api/v2/categories",
                            headers=self.headers,
                            data=json.dumps(self.category))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "The category name is required"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)

    def test_create_duplicate_category(self):
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/categories",
                      headers=self.headers,
                      data=json.dumps(self.category))
        res = self.app.post("/api/v2/categories",
                            headers=self.headers,
                            data=json.dumps(self.category))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Category with this name exists"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, expected_output)

    def test_create_category_authenticated_as_store_attendant(self):
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers,
                      data=json.dumps(self.reg_data))
        res = self.app.post("/api/v2/auth/login",
                            headers=self.headers,
                            data=json.dumps(self.login_data))
        self.headers["Authorization"] = "Bearer " + json.loads(res.data)["token"]
        res = self.app.post("/api/v2/categories",
                            headers=self.headers,
                            data=json.dumps(self.category))
        res_data = json.loads(res.data)
        expected_output = {
            "error": "Please login as a store owner"
        }
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res_data, expected_output)

    def test_create_category_unauthenticated(self):
        res = self.app.post("/api/v2/categories",
                            headers=self.headers,
                            data=json.dumps(self.category))
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
