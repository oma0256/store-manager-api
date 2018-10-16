import unittest
import json
from api.__init__ import app
from api import views

class TestStoreOwnerAuth(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.reg_data = {
            "first_name": "joe",
            "last_name": "doe",
            "email": "joe@email.com",
            "password": "pass1234",
            "confirm_password": "pass1234"
        }
    
    def tearDown(self):
        views.store_owners = []

    def test_register_valid_data(self):
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
        
