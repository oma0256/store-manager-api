"""
File to generate an id
"""


def create_id(item_list):
    """
    Function to create a new id
    """
    if not item_list:
        return 1
    new_id = item_list[-1].id + 1
    return new_id
