#!/usr/bin/python3
"""count by type"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, State, Amenity
import models


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """ return all amenities """
    amenities = storage.all("Amenity")
    L_amenities = []
    for key in amenities:
        L_amenities.append(amenities[key].to_dict())

    return (jsonify(L_amenities))


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def amenities_id(amenity_id):
    """ return an amenity by id """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is not None:
        return (jsonify(amenity.to_dict()))
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_id(amenity_id):
    """ delete an amenity by id """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenities():
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
    new_amenity = Amenity(**req)
    storage.new(new_amenity)
    storage.save()
    return(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """ actualice an amenity by his id """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
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
            setattr(amenity, key, value)
    storage.save()
    storage.close()
    return(jsonify(amenity.to_dict()), 200)
