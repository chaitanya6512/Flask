from flask import Flask
app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Hello, Welcome to Flask App Routing"
  
@app.route("/")
def index():
    return "Homepage of Flask App Routing"

if __name__ == "__main__":
    app.run(debug=True)