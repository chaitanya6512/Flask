from flask import Flask, make_response, request
app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def vistiors_count():
    count = int(request.cookies.get('vistiors count', 0))
    count = count+1
    output = 'You visited this page for' +str(count)+'times'
    resp = make_response(output)
    resp.set_cookie('visitiors count', str(count))
    return resp

@app.route('/get')
def get_visitors_count():
    count = request.cookies.get('visitors count')
    return count

app.run()