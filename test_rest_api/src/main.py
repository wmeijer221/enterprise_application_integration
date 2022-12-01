#!/usr/bin/env python

import json
from flask import Flask, jsonify
from flask_restful import Resource, request, Api, reqparse
from flask_cors import CORS


class GetTest(Resource):

    def get(self):
        ofTheJedi = jsonify({
            "message": "Hello World!",
            "test": "test-value"
            })
        return ofTheJedi

class GetAPIStatus(Resource):

    def get(self):
        ofTheJedi = "Online"
        return ofTheJedi


if __name__ == '__main__':

    app = Flask(__name__)
    api = Api(app)

    api.add_resource(GetAPIStatus, '/')
    api.add_resource(GetTest, '/test')


    cors = CORS(app)

    app.run(host='0.0.0.0', port=5000, debug=True)