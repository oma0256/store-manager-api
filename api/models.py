"""
Create application models
"""


class User:
    """
    Define user structure
    """
    def __init__(self, **kwargs):
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
        self.name = kwargs.get("name")
        self.unit_cost = kwargs.get("unit_cost")
        self.quantity = kwargs.get("quantity")


class Sale:
    """
    Define sale structure
    """
    def __init__(self, cart_items,
                 attendannt, total):
        self.cart_items = cart_items
        self.attendant = attendannt
        self.total = total

class Category:
    """
    Define Category structure
    """
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
