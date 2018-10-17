"""
File to test product view
"""

import unittest
import json
from api import views
from api.__init__ import app


class TestSaletView(unittest.TestCase):
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
            "quantity": 1
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
