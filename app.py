import json
import threading
from index import ARK
from flask_cors import CORS
from flask import Flask, request
from flask_restful import Api, Resource
from shared.models.interfaces import ChatInput, Output

app = Flask(__name__)
api = Api(app)
CORS(app)


class ARKResource(Resource):

    def post(self) -> dict:
        input = json.loads(request.get_data())
        print(input, '__input__')
        input = ChatInput(**input)
        ark_obj = ARK(input)
        if input.send_reply == True:
            threading.Thread(target=ark_obj.compute).start()
            output = Output(output_message="Ark is processing your request")
        else:
            output = ark_obj.compute()

        return output.__dict__


api.add_resource(ARKResource, '/ark')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
