import os
from flask import Flask, jsonify, request

import numpy as np
from arima_model import forecast

def flask_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def server_is_up():
        return 'Ahh, success! Da server--she is up and runnings now, ja! Very good, very good.'

    @app.route('/forecast', methods=['POST'])
    def start():
        to_model = request.json

        print(to_model)
        fore = forecast(**to_model)
        return jsonify({'forecast': fore.tolist()})
    return app

if __name__ == '__main__':
    app = flask_app()
    app.run(debug=True, host='0.0.0.0', port=5001)