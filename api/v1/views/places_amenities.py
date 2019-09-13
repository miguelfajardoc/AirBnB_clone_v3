#!/usr/bin/python3
"""count by type"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, State, Amenity
import models


@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def place_amenity(place_id):
    """ return all amenity belongs to a place """

    place = storage.get("Place", place_id)
    amenity_list = []
    if place is None:
        abort(404)
    if models.storage_t == 'db':
        amenities = models.place.place_amenity
        return jsonify(list(map(lambda y: y.to_dict(), place.amenities)))
    else:
        amenities = models.place.amenities
        return (jsonify(amenity_list))
    print(list(amenities))



@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_place(place_id, amenity_id):
    """ delete an amenity in some place """

    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if models.storage_t != 'db':
        amenities = place.amenity
        for ameni in amenities:
            if amenity.id == ameni:
                amenities.remove(ameni)
                return jsonify({})
        abort(404)
    else:
        amenities = place.amenities
        for ameni in amenities:
            if amenity.id in ameni and place.id in ameni:
                storage.delete(ameni)
                storage.save()
                return jsonify({})
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_amenity_place(place_id, amenity_id):
    """use the post method to create a relation amenity"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if models.storage_t != 'db':
        amenities = place.amenity
        for ameni in amenities:
            if amenity.id == ameni:
                return jsonify(amenity.to_dic())
            else:
                place.amenities.append(amenity)
                return jsonify(amenity.to_dic()), 201
    else:
        all_amenities =list(map(lambda y: y.to_dict(), place.amenities))
        for ameni in all_amenities:
            if amenity.id in ameni and place.id in ameni:
                return jsonify(amenity.to_dic())
            else:
                place.amenities.append(amenity)
                return jsonify(amenity.to_dic()), 201
