from flask import Flask

app = Flask(__name__)
@app.route('/')
def msg():
    return "Welcome to Flask Tutorial"

@app.route('/vfloat/<float:balance>')
def vfloat(balance):
    return "My Account Balance is %f" %balance


app.run(debug=True)