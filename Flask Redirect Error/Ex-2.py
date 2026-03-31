from flask import Flask, abort

app = Flask(__name__)
@app.route('/')
def demo():
    return 'Welcome to Flask Tutorial'

@app.route('/<username>')
def hello_user(username):
    if username[0].isdigit():
        abort(403)
    return '<h1>Good Username</h1>'

if __name__ == '__main__':
    app.run(debug=True)