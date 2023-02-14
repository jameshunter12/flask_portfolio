from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.activity import Activities

activity_api = Blueprint('activity_api', __name__,
                   url_prefix='/api/activities')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(activity_api)

class ActivityAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 210
            # look for password and dob
            address = body.get('address')
            if name is None or len(address) < 2:
                return {'message': f'Address is missing, or is less than 2 characters'}, 210
            coordinates = body.get('coordinates')
            if name is None or len(coordinates) < 2:
                return {'message': f'Coordinates is missing, or is less than 2 characters'}, 210
            fun = body.get('fun')
            if name is None or len(fun) < 2:
                return {'message': f'Fun is missing, or is less than 2 characters'}, 210
            
            ''' #1: Key code block, setup USER OBJECT '''
            uo = Activities(name=name, 
                      uid=uid)
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            Activity = uo.create()
            # success returns json of user
            if activity:
                return jsonify(activity.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            Activities = Activities.query.all()    # read/extract all users from database
            json_ready = [Activity.read() for user in Activites]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')