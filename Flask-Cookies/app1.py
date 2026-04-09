from flask import Flask, request, make_response, render_template
app = Flask(__name__)

@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/details', methods=['GET','POST'])
def details():
    if request.method == 'POST':
        name = request.form['username']
        output = 'Hi, Welcome '+name+''
        resp = make_response(output)
        resp.set_cookie('username', name)
    return resp

if __name__ == "__main__":
    app.run(debug=True)