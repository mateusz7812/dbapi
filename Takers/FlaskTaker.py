import json
import sys

from Takers.TakerInterface import Taker
from flask import Flask, request, Response, make_response, jsonify
from flask_cors import CORS

print_results = True
flaskTaker = None


class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={
            'Access-Control-Allow-Origin': '*'
        })

    def __call__(self, *args):
        self.response.data = self.action()
        return self.response


class FlaskAppWrapper(object):
    app = None

    def __init__(self, name):
        self.app = Flask(name)
        CORS(self.app)
        self.app.secret_key = 'super secret key'
        self.app.config['SESSION_TYPE'] = 'filesystem'

    def run(self):
        self.app.run(host="0.0.0.0", port=7000)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler), methods=methods)


def action():
    if request.method == "POST":
        data = request.data.decode("utf-8")
        loaded_data = json.loads(data)
        try:
            response = flaskTaker.take(loaded_data)
        except Exception as exc:
            print("ERROR", "POST request", data)
            raise exc
        if print_results:
            print("POST request", data, "\n response", response)
            sys.stdout.flush()
        response = json.dumps(response)
        return bytes(response, "utf-8")
    return bytes("Hello, i am working!", "utf-8")


class FlaskTaker(Taker):
    def start(self):
        global flaskTaker
        flaskTaker = self
        a = FlaskAppWrapper('wrap')
        a.add_endpoint(endpoint='/', endpoint_name='main', handler=action, methods=["GET", "POST"])
        a.run()

    def stop(self):
        pass
