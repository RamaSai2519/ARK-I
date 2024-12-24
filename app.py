import json
from index import ARK
from flask_cors import CORS
from flask import Flask, request
from flask_restful import Api, Resource
from shared.models.interfaces import ChatInput

app = Flask(__name__)
api = Api(app)
CORS(app)


class ARKResource(Resource):

    def post(self) -> dict:
        input = json.loads(request.get_data())
        input = ChatInput(**input)
        output = ARK(input).compute()

        return output.__dict__


api.add_resource(ARKResource, '/ark')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
