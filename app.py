from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import utils

app = Flask(__name__)
api = Api(app)


class Index(Resource):
    @staticmethod
    def get():
        return jsonify(message="captcha resolver endpoint...")


class Predict(Resource):
    @staticmethod
    def get():
        return jsonify(message="send a post request...")

    @staticmethod
    def post():
        json_data = request.get_json(force=True)
        img_uri = json_data['uri']
        result = predictor.predict(img_uri)
        return jsonify(message="success", result=result)


api.add_resource(Predict, '/predict')
api.add_resource(Index, '/')

if __name__ == '__main__':
    predictor = utils.Predictor()
    app.run()
