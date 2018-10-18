"""
Define product model
"""

class Product:
    """
    Define product structure
    """
    def __init__(self, product_id, name, price, quantity, category):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category