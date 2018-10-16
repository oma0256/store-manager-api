"""
Create application models
"""


class User:
    """
    Define user structure
    """
    def __init__(self, user_id, first_name, last_name, email, password, is_admin):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
