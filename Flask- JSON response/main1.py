# 2. flask_restful() method

from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)

api = Api(app)

class returnjson(Resource):
    def get(self):
        data = {
            "Modules":  15,
            "Subjects": "Data Structures and Algorithms"
        }
        return data
    
api.add_resource(returnjson,'/returnjson')

if __name__ == "__main__":
    app.run(debug=True)