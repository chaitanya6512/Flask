from flask import Flask

app = Flask(__name__)

@app.route('/')
def demo():
    return "Welcome"

@app.route('/vint/<int:age>')
def vint(age):
    return "This is Thomas. I am %d years old" % age

app.run(debug=True)