from flask import Flask

app = Flask(__name__)

@app.route('/post/<int:id>')
def changedtype(id):
    return f'This post has the id{id}'

@app.route('/hello')
def hello():
    return 'Hello, Welcome to ChangeDataType Converter'

@app.route('/')
def demo():
    return "Homepage of Change Data Type Converter"

if __name__ == '__main__':
    app.run(debug=True)