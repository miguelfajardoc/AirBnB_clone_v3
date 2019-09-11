#!/usr/bin/python3
"""count by type"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, State, City
import models


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_state():
    """ return all cities of an states """
    states = state.get("State", state_id)
    if states is None:
        abort(404)
    state_cities = []
    for key in states.cities:
        state_cities.append(city[key].to_dict())
    return (jsonify(state_cities))


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_id(state_id):
    """ return a city by id """
    city = storage.get("City", city_id)
    if city is not None:
        return (jsonify(city.to_dict()))
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_id(state_id):
    """ delete a city by id """
    city = storage.get("State", city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
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
    state = state.get("State", id)
    if state is None:
        abort(404)
    new_city = City()
    new_city.state_id = id
    new_city.name = name
    new_city.save()
    return(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """ update a city by his id """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    try:
        if not request.is_json:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        req = request.get_json()
    except:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in req.items():
        if key is not 'id' and key is not 'created_at' and key is not\
           'updated_at':
            setattr(state, key, value)
    storage.save()
    storage.close()
    return(jsonify(city.to_dict()), 200)
