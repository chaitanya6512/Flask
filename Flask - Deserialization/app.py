# Deserialization Method 1: Using request.get_json()

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/data')
def get_data():
    data = {"name": "Alice", "age":25}
    return jsonify(data)

@app.route('/submit', methods=['POST'])
def receive_data():
    data = request.get_json()
    return jsonify({"message":"Data received", "data":data})

if __name__ == "__main__":
    app.run(debug=True)