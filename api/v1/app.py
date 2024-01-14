#!/usr/bin/python3
"""
Flask application that integrates with AirBnB static HTML Template.
"""


from os import environ
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(error):
    """
    Removes the current SQLAlchemy Session object after each request.
    """
    storage.close()


# error handler 404 for unexpected behavior
@app.errorhandler(404)
def not_found(error):
    """
    Return error message `Not Found`.
    """
    response = {'error': 'Not found'}
    return jsonify(response), 404


if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
