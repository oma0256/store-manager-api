"""
File contains funtions to use on my products and sales
"""
from flask import jsonify


def get_single_resource(resource_list, resource_id, msg, key):
    """
    Iterates through product and sale to return a single object
    """
    for resource in resource_list:
        # check if sale record or product exists
        if resource.id == int(resource_id):
            return jsonify({
                "message": msg,
                key: resource.__dict__
            })
    if key == "products":
        return jsonify({"error": "This product does not exist"}), 404
    if key == 'sale':
        return jsonify({"error": "Sale record with this id doesn't exist"}), 404
