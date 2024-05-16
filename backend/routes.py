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
    return jsonify(data),200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if id is not None and data is not None:
        for pic in data:
            if pic['id']==id:
                return pic,200
    return {'Message':"No picture found"},404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.json
    if data is not None:
        for pic in data:
            if picture['id'] is not None:
                if pic['id']==picture['id']:
                    return {"Message": f"picture with id {picture['id']} already present"},302
        data.append(picture)
        return picture,201
    return {'Message':"Server error"},404

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.json
    if id is not None and data is not None:
        for i,pic in enumerate(data):
            if pic['id']==id:
                data[i] = picture
                return {'Message':"Picture updated"},201
    
    return {'Message':'Picture does not exist'},404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if id is not None and data is not None:
        for i,pic in enumerate(data):
            if pic['id']==id:
                data.remove(pic)
                return "",204
        
    return {'Message':'Picture does not exist'},404
