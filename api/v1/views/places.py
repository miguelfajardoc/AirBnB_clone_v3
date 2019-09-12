#!/usr/bin/python3
"""count by type"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, State, City, Place
import models


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def city_place(city_id):
    """ return all places of a city """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city_places = []
    for place in city.places:
        city_places.append(place.to_dict())
    return (jsonify(city_places))


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_id(place_id):
    """ return a city by id """
    place = storage.get("Place", place_id)
    if place is not None:
        return (jsonify(place.to_dict()))
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    """ delete a place by id """
    place = storage.get("Place", place_id)
    if place_id is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """use the post method to create"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    try:
        if not request.is_json:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        req = request.get_json()
    except:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    user_id = req.get("user_id")
    if user_id is None:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    dict_name = req.get("name")
    if dict_name is None:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    req["city_id"] = city_id
    new_place = Place(**req)
    storage.new(new_place)
    new_place.save()
    return(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_Place(place_id):
    """ update a place by his id """
    place = storage.get("Place", place_id)
    exceptions = ["id", "user_id", "created_at", "updated_at", "city_id"]
    if place is None:
        abort(404)
    try:
        if not request.is_json:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        req = request.get_json()
    except:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in req.items():
        if key not in exceptions:
            setattr(place, key, value)
    storage.save()
    storage.close()
    return(jsonify(place.to_dict()), 200)
