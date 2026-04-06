# Creating Custom WSGI Middleware

class WSGILoggingMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print(f"Incoming request:{environ['REQUEST_METHOD']} {environ['PATH_INFO']}")
        return self.app(environ, start_response)
    
from flask import Flask

app = Flask(__name__)

# Applying the WSGI Middleware
app.wsgi_app = WSGILoggingMiddleware(app.wsgi_app)

@app.route('/')
def home():
    return "Hello, WSGI Middleware!"

if __name__ == "__main__":
    app.run(debug=True)