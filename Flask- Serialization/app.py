# Serialization Method 1: Using Flask's jsonify

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/data')
def get_data():
    data = {"name":"Alice", "age":25}
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)