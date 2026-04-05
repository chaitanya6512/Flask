# Creating Custom Middleware in Flask


from flask import Flask, request

app = Flask(__name__)

@app.before_request
def log_request():
    print(f"Incoming request:{request.method} {request.url}")

@app.after_request
def log_response(response):
    print(f"Outgoing response:{response.status_code}")
    return response

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)


# Explanation:
# 1.@app.before_request: Middleware that handles incoming requests()
# log_request() - Runs before each request.
# Prints the HTTP method and request url.

# 2.@app.after_request: Middleware that handles outgoing responses()
# log_responses(response) - Runs after each request.
# Returns response to complete the request cycle.