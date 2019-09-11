#!/usr/bin/python3
"""count by type"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, State
import models


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ return all states """
    states = storage.all("State")
    L_state = []
    for key in states:
        L_state.append(states[key].to_dict())

    return (jsonify(L_state))


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_id(state_id):
    """ return an state by id """
    state = storage.get("State", state_id)
    if state is not None:
        return (jsonify(state.to_dict()))
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_id(state_id):
    """ delete an state by id """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """use the post method to create"""
    try:
        if not request.is_json:
             return make_response(jsonify({'error': 'Not a JSON'}), 400)
        req = request.get_json()
    except:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    dict_name = req.get("name")
    if dict_name is None:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_state = State(**req)
    return(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ actualice an state by his id """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    try:
        req = request.get_json()
    except:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in req.items():
        if key is not 'id' and key is not 'created_at' and key is not\
           'updated_at':
            setattr(state, key, value)
    storage.save()
    storage.close()
    return(jsonify(state.to_dict()), 200)
