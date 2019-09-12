#!/usr/bin/python3
"""count by type"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, State, City, Review
import models


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def places_reviews(place_id):
    """ return all reviews of a place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews_place = []
    for review in place.reviews:
        reviews_place.append(review.to_dict())
    return (jsonify(reviews_place))


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_id(review_id):
    """ return a review by id """
    review = storage.get("Review", review_id)
    if review is not None:
        return (jsonify(review.to_dict()))
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_delete(city_id):
    """ delete a review by id """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_post(place_id):
    """use the post method to create"""
    try:
        if not request.is_json:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        req = request.get_json()
    except:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    user_id = req.get("user_id")
    if user_id is None:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    text = req.get("text")
    if text is None:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    place = storage.get("Place", place_id)
    user = storage.get("User", user_id)
    if place is None or user is None:
        abort(404)
    req["place_id"] = place_id
    new_review = Review(**req)
    storage.new(new_review)
    storage.save()
    return(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def review_city(review_id):
    """ update a review by his id """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    try:
        if not request.is_json:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        req = request.get_json()
    except:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in req.items():
        if key is not 'id' and key is not 'created_at' and key is not\
           'updated_at' and key is not 'user_id' and key is not\
           'place_id':
            setattr(review, key, value)
    storage.save()
    storage.close()
    return(jsonify(city.to_dict()), 200)
