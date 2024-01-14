#!/usr/bin/python3
"""
Create a route `/status` on the object app_views.
"""


from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Returns a JSON response for RESTful API health.
    """
    response = {'status': 'OK'}
    return jsonify(response)
