from flask import Flask

app = Flask(__name__)

@app.route('/user/<username>')
def show_name(username):
    return f' Hello {username} !'

@app.route('/hello')
def hello():
    return 'Hello, Welcome to Flask Dynamic URLs'

@app.route('/')
def demo():
    return 'Homepage of Flask Dynamic URLs'

if __name__ == '___main__':
    app.run(debug=True)