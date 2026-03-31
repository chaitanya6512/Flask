from flask import Flask

app = Flask(__name__)

@app.route('/')
def msg():
    return 'Welcome'

@app.route('/vstring/<name>')
def string(name):
    return "My Name is %s" % name

app.run(debug=True)



# Explaination
# @app.route('/') - Defines the homepage route that returns a welcome message
# @app.route('/vstring/<name>') - A dynamic route that takes a string parameter and displays it in a message
# app.run(debug=True) - Runs the Flask app with debugging enabled


