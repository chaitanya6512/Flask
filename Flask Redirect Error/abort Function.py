from flask import Flask, abort

app = Flask(__name__)

@app.route('/<uname>')
def index(uname):
    if uname[0].isdigit():
        abort(400)
    return '<h1>Good Username</h1>'

if __name__ == '__main__':
    app.run(debug=True)