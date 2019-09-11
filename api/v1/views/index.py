#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
import models


@app_views.route('/status', strict_slashes=False)
def status():
    """returns ok"""
    return (jsonify({"status": "OK"}))


@app_number_of_objects.route('/api/v1/stats', strict_slashes=False)
def endpoint():
    """define an endpoint that retrives the number
       of objects by type"""
    return (jsonify({"amenities": storage.count("Amenity"),
                     "cities": storage.count("City"),
                     "places": storage.count("Place"),
                     "reviews": storage.count("Review"),
                     "states": storage.count("State"),
                     "users": storage.count("User")}))
