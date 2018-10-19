"""
Create application models
"""


class User:
    """
    Define user structure
    """
    def __init__(self, user_id, first_name, last_name,
                 email, password, is_admin):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin


class Product:
    """
    Define product structure
    """
    def __init__(self, product_id, name, price, quantity, category):
        self.id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category


class Sale:
    """
    Define sale structure
    """
    def __init__(self, sale_id, cart_items,
                 attendannt_email, total):
        self.id = sale_id
        self.cart_items = cart_items
        self.attendant_email = attendannt_email
        self.total = total
