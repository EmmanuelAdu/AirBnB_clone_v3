#!/usr/bin/python3
"""
Create new view for State objects that handles all default RESTFul API actions
"""


from flask import abort, jsonify, make_response, request
from storage.state import State
from api.v1.views import app_views
from models import storage


# Route for retrieving all list of State objects
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """
    Retrieves all list of State objects from storage
    """
    # Get all states objects from  the storage
    states = storage.all(State).values()
    # Convert object to dict and jsonify the list
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


# Route for retrieving a specific State object by ID
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object by state id
    """
    state = storage.get(State, state_id)
    if state:
        # Return the State object in JSON Format
        return jsonify(state.to_dict())
    else:
        # Return 404 error if State is not found
        abort(404)


# Route for deleting a specific State by ID
@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    Deleting a specific State by state id from storage
    """
    state = storage.get(State, state_id)
    if state:
        # Delete the specified state object and save changes
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        # Return 404 error not found if state object not found
        abort(404)


# Route for creating a new state object
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creating a new state object
    """
    if not request.get_json():
        # Return 400 error if request is not in JSON Format
        abort(400, 'Not a JSON')

    # Get the keyword arg from the request
    kwargs = request.get_json()
    if 'name' not in kwargs:
        # Return 400 error if 'name' key is missing in JSON DATA
        abort(400, 'Missing name')

    # Create a new State object from the JSON data
    state = State(**kwargs)
    # save the State object to the storage
    state.save()
    # Return the newly created State object in jsonify
    return make_response(jsonify(state.to_dict(), 201))


# Route for updating an existing State object by ID
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slahes=False)
def update_state(state_id):
    """
    Updates a State object
    """
    # Get the state object from the storage by state id
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            # Request 400 error if the data request is not json format
            abort(400, 'Not a JSON')
    # Get the json data from the request
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    # Update the attributes of the State object with the JSON data
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)

    # Save the updated state object to the storage
    state.save()
    # Return the updated state object in JSON Format with 200 status code
    return make_response(jsonify(state.to_dict()), 200)
