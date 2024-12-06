import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/items', methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        response = requests.get('http://nginx/items')
    elif request.method == 'POST':
        response = requests.post('http://nginx/items', json=request.json)
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
