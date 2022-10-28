from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import predictor

app = Flask(__name__)
api = Api(app)

class Index(Resource):
    def get(self):
        return jsonify(message="captcha resolver endpoint...")

class Predict(Resource):
    def get(self):
        return jsonify(message="send a post request...")

    def post(self):
        json_data = request.get_json(force=True)
        img_uri = json_data['uri']
        result = instance.predict(img_uri)
        return jsonify(message="success", result=result)

api.add_resource(Predict,'/predict')
api.add_resource(Index,'/')

if __name__ == '__main__':
    instance = predictor.Predictor()
    app.run()