from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
from threading import Thread


# from gunicorn import glogging


# code for endpoints
from nlp import NLP

app = Flask(__name__)
api = Api(app)

class Index(Resource):
    def get(self):
        return make_response(
                jsonify(
                    {
                        'message': 'Welcome to the API for V-Unite. Status is OKAY!'
                        }), 
                    200)
# API Endpoints
api.add_resource(Index, '/api/', methods=['GET'])

#For Questions & Answers
api.add_resource(NLP, '/api/input', methods=['GET'])

if __name__ == '__main__':
    # run app with os environment host and port

    app.run(threaded = True)