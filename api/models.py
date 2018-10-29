"""
Create application models
"""


class User:
    """
    Define user structure
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get("user_id")
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")
        self.is_admin = kwargs.get("is_admin")


class Product:
    """
    Define product structure
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get("product_id")
        self.name = kwargs.get("name")
        self.unit_cost = kwargs.get("unit_cost")
        self.quantity = kwargs.get("quantity")


class Sale:
    """
    Define sale structure
    """
    def __init__(self, sale_id, cart_items,
                 attendannt, total):
        self.id = sale_id
        self.cart_items = cart_items
        self.attendant = attendannt
        self.total = total
