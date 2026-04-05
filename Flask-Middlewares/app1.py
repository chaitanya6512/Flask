# Middleware for Authentication and Authorization

from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = 'my_secret_api_key'

@app.before_request
def check_authentication():
    token = request.headers.get('Authentication')
    if token != f'Bearer{API_KEY}':
        return jsonify({"error":"Unauthorized"}), 401
    
@app.route('/protected')
def protected():
    return jsonify({'message': "Welcome to the protected route!"})

if __name__ == "__main__":
    app.run(debug=True)



# Explanation
# 1. before_request Middleware
# Extracts the Authorization token from request headers.
# If the token is missing or incorrect, returns 401 Unauthorized.

# 2./protected - route that can only be accessed if a valid token is provided. 