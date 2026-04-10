# There are 2 ways to build a simple Flask REST API that returns a JSON response.
# jsonify() Function:

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/returnjson', methods=['GET'])
def return_json():
    if request.method == 'GET':
        data = {
            "modules": 15,
            "subject": "Data Structures and algorithms"
        }
        return jsonify(data)
    
if __name__ == "__main__":
    app.run(debug=True)