import unittest
import json
from api import views
from api.__init__ import app
from db import DB
app.config.from_object('config.TestConfig')

class TestProductView(unittest.TestCase):
    """
    Class to test product view
    """
    # def create_app(self):
    #     app.config.from_object('config.TestConfig')
    #     return app

    def setUp(self):
        self.app = app.test_client()
        self.db_conn = DB()
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
        self.access_token = json.loads(response.data)["token"]
        self.category = {
            "name": "Tech",
            "description": "This is tech"
        }

    def tearDown(self):
        self.db_conn.delete_categories()

    def test_create_category_with_valid_data(self):
        self.headers["Authorization"] = "Bearer " + self.access_token
        res = self.app.post("/api/v2/categories",
                            headers=self.headers,
                            data=json.dumps(self.category))
        res_data = json.loads(res.data)
        expected_output = {
            "message": "Successfully created product category",
            "category": self.category
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

    def test_modify_category_as_store_owner(self):
        """
        Test modify a category with valid data
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/categories",
                      headers=self.headers,
                      data=json.dumps(self.category))
        category_id = self.db_conn.get_categories()[0]["id"]
        self.category["name"] = "svdkjsd"
        res = self.app.put("/api/v2/categories/" + str(category_id),
                           headers=self.headers,
                           data=json.dumps(self.category))
        res_data = json.loads(res.data)
        exepected_output = {
            "message": "Category updated successfully",
            "category": self.category
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data, exepected_output)
    
    def test_modify_category_as_store_attendant(self):
        """
        Test modify a category as store attendant
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/categories",
                      headers=self.headers,
                      data=json.dumps(self.category))
        category_id = self.db_conn.get_categories()[0]["id"]
        self.category["name"] = "svdkjsd"
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers,
                      data=json.dumps(self.reg_data))
        res = self.app.post("/api/v2/auth/login",
                      headers=self.headers,
                      data=json.dumps(self.login_data))
        self.headers["Authorization"] = "Bearer " + json.loads(res.data)["token"]
        res = self.app.put("/api/v2/categories/" + str(category_id),
                           headers=self.headers,
                           data=json.dumps(self.category))
        res_data = json.loads(res.data)
        exepected_output = {
            "error": "Please login as a store owner"
        }
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res_data, exepected_output)
    
    def test_modify_category_non_existant(self):
        """
        Test modify a category which doesn't exist
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/categories",
                      headers=self.headers,
                      data=json.dumps(self.category))
        self.category["name"] = "svdkjsd"
        res = self.app.put("/api/v2/categories/553445354665789",
                           headers=self.headers,
                           data=json.dumps(self.category))
        res_data = json.loads(res.data)
        exepected_output = {
            "error": "The category you're trying to modify doesn't exist"
        }
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data, exepected_output)

    def test_modify_category_with_empty_value(self):
        """
        Test modify a category with empty value
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/categories",
                      headers=self.headers,
                      data=json.dumps(self.category))
        category_id = self.db_conn.get_categories()[0]["id"]
        self.category["name"] = ""
        res = self.app.put("/api/v2/categories/" + str(category_id),
                           headers=self.headers,
                           data=json.dumps(self.category))
        res_data = json.loads(res.data)
        exepected_output = {
            "error": "The category name is required"
        }
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data, exepected_output)

    def test_delete_category_store_owner(self):
        """
        Test delete a category as store owner
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/categories",
                      headers=self.headers,
                      data=json.dumps(self.category))
        category_id = self.db_conn.get_categories()[0]["id"]
        res = self.app.delete("/api/v2/categories/" + str(category_id),
                           headers=self.headers,
                           data=json.dumps(self.category))
        res_data = json.loads(res.data)
        exepected_output = {
            "message": "Category has been deleted successfully"
        }
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data, exepected_output)
    
    def test_delete_category_store_attendant(self):
        """
        Test delete a product as store attendant
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/categories",
                      headers=self.headers,
                      data=json.dumps(self.category))
        category_id = self.db_conn.get_categories()[0]["id"]
        self.app.post("/api/v2/auth/signup",
                      headers=self.headers,
                      data=json.dumps(self.reg_data))
        res = self.app.post("/api/v2/auth/login",
                            headers=self.headers,
                            data=json.dumps(self.login_data))
        self.headers["Authorization"] = "Bearer " + json.loads(res.data)["token"]
        res = self.app.delete("/api/v2/categories/" + str(category_id),
                              headers=self.headers)
        res_data = json.loads(res.data)
        exepected_output = {
            "error": "Please login as a store owner"
        }
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res_data, exepected_output)
    
    def test_delete_category_non_existance(self):
        """
        Test delete a category as store owner
        """
        self.headers["Authorization"] = "Bearer " + self.access_token
        self.app.post("/api/v2/categories",
                      headers=self.headers,
                      data=json.dumps(self.category))
        res = self.app.delete("/api/v2/categories/142556789068970",
                           headers=self.headers,
                           data=json.dumps(self.category))
        res_data = json.loads(res.data)
        exepected_output = {
            "error": "Category you're trying to delete doesn't exist"
        }
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data, exepected_output)
