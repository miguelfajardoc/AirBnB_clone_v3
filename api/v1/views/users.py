#!/usr/bin/python3
"""count by type"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, User
import models


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """ return all users """
    users = storage.all("User")
    users_list = []
    for user in users:
        users_list.append(users[user].to_dict())
    return (jsonify(users_list))


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_id(user_id):
    """ return a user by id """
    user = storage.get("User", user_id)
    if user is not None:
        return (jsonify(user.to_dict()))
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def user_delete(user_id):
    """ delete a user by id """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_post():
    """use the post method to create"""
    try:
        if not request.is_json:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        req = request.get_json()
    except:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    dict_email = req.get("email")
    if dict_email is None:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    dict_password = req.get("password")
    if dict_password is None:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    new_user = User(**req)
    new_user.save()
    return(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ update a user by his id """
    user = storage.get("User", user_id)
    exceptions = ["id", "created_at", "updated_at", "email"]
    if user is None:
        abort(404)
    try:
        if not request.is_json:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        req = request.get_json()
    except:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in req.items():
        if key not in exceptions:
            setattr(user, key, value)
    storage.save()
    storage.close()
    return(jsonify(user.to_dict()), 200)
