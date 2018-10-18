"""
File to test the application models
"""

import unittest
from api.models import User, Product, Sale


class TestModels(unittest.TestCase):
    """
    Test app models
    """
    def test_user_model(self):
        """
        Test initializing a User object
        """
        user = User(1, "first", "last", "first@email.com", "pass1234", True)
        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.first_name, "first")
        self.assertEqual(user.last_name, "last")
        self.assertEqual(user.email, "first@email.com")
        self.assertEqual(user.password, "pass1234")
        self.assertEqual(user.is_admin, True)

    def test_product_model(self):
        """
        Test initializing a Product object
        """
        product = Product(1, "Belt", 10000, 3, "clothing")
        self.assertEqual(product.product_id, 1)
        self.assertEqual(product.name, "Belt")
        self.assertEqual(product.price, 10000)
        self.assertEqual(product.quantity, 3)
        self.assertEqual(product.category, "clothing")

    def test_sale_model(self):
        """
        Test initializing a Sale object
        """
        product = {
            "name": "Belt",
            "quantity": 1,
            "price": 10000
        }
        sale = Sale(1, [product], "joe doe", "joe@email.com", 10000)
        self.assertEqual(sale.sale_id, 1)
        self.assertEqual(sale.products, [product])
        self.assertEqual(sale.attendant_name, "joe doe")
        self.assertEqual(sale.attendant_email, "joe@email.com")
        self.assertEqual(sale.total, 10000)
