# import unittest
# import json
# from api import views

# class TestProductView(unittest.TestCase):
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
#         self.product = {
#             "name": "Belt",
#             "price": 10000,
#             "quantity": 3
#         }

#     def tearDown(self):
#         views.products = []

#     def test_create_product_with_valid_fields(self):
#         self.app.post("/api/v1/store-owner/register",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.reg_data))
#         self.app.post("/api/v1/store-owner/login",
#                       headers={"Content-Type": "application/json"},
#                       data=json.dumps(self.login_data))
#         res = self.app.post("/api/v1/products",
#                             headers={"Content-Type": "application/json"},
#                             data=json.dumps(self.product))
#         res_data = json.loads(res.data)
#         self.product["id"] = 1
#         expected_output = {
#             "message": "Product created successfully",
#             "product": self.product
#         }
#         self.assertEqual(res.status_code, 201)
#         self.assertEqual(res_data, expected_output)
