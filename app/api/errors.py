from flask import jsonify
from app.exceptions import ValidationError
from . import api

def badrequest(message):
    response = jsonify({"error":"Bad request",'message':'message'})
    response.status_code = 400
    return response

def unauthorized(message):
    response = jsonify({"error":"Unauthorized",'message':'message'})
    response.status_code = 401
    return response

def forbidden(message):
    response = jsonify({"error":"Forbidden",'message':'message'})
    response.status_code = 403
    return response

def methodnotfound(message):
    response = jsonify({"error":"Method Not Found",'message':'message'})
    response.status_code = 405
    return response

@api.errorhandler(ValidationError)
def validation_error(e):
    return badrequest(e.args[0])