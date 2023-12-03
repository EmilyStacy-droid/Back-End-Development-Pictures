from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200
    return {"message": "no pictures"}, 404

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for picture in data:
            if int(picture['id']) == id:
                return jsonify(picture), 200
        return {"message": "Picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.json
    if not new_picture:
        return {"message": "Invalid input parameter"}, 422

    try:
        for picture in data:
            if picture['id'] == new_picture['id']:
                return {"Message": f"picture with id {new_picture['id']} already present"}, 302
        data.append(new_picture)
        result = int(f"{new_picture['id']}")
        return {"id": result}, 201
    except NameError:
        return {"message": "data not defined"}, 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_picture = request.json
    for picture in data:
        if picture['id'] == id:
            if new_picture.get('pic_url') is not None:
                picture['pic_url'] = new_picture['pic_url']
            if new_picture.get('event_country') is not None:
                picture['event_country'] = new_picture['event_country']
            if new_picture.get('event_state') is not None:
                picture['event_state'] = new_picture['event_state']
            if new_picture.get('event_city') is not None:
                picture['event_city'] = new_picture['event_city']
            if new_picture.get('event_date') is not None:
                picture['event_date'] = new_picture['event_date']
            return jsonify(picture), 200

    return {"message": "id not found"}, 404
######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if picture['id'] == id:
            data.remove(picture)
            return "", 204
    return {"message": "picture not found"}, 404
