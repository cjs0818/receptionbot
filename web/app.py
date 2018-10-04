# app.py
from flask import Flask, request

import json

app = Flask('app')


@app.route('/')
def index():
    return "I'm from docker"

@app.route('/message', methods=['POST'])
def message():
    req = request.get_json()

    res = {
        'answer': 'OK'
    }
    print (res)
    return jsonify(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=60000, debug=True)
