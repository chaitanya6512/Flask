# Using marshmallow for Serialization and Deserialization
from flask import Flask, request, jsonify
from marshmallow import Schema, fields 

app = Flask(__name__)

# Define a Schema
class UserSchema(Schema):
    username=fields.String(required=True)
    email = fields.String(required=True)

user_schema = UserSchema()
@app.route('/validate', methods=['POST'])
def validate_user():
    json_data = request.get_json()
    errors = user_schema.validate(json_data)

    if errors:
        return jsonify(errors)
    return jsonify({"message":"Valid data", "data":json_data})

if __name__ == "__main__":
    app.run(debug=True)