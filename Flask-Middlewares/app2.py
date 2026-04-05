# Third-Party Middleware in Flask

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Allows requests only from specific frontend origins
CORS(app, origins=["http://localhost:3000", "https://myfrontend.com/"])

@app.route('/public_data')
def public_data():
    return jsonify({'message':"This data is accessible from allowed origins."})


@app.route('/public_data')
def public_data():
    return jsonify({'message':"This data is accessible from allowed origins."})


if __name__ == "__main__":
    app.run(debug=True)