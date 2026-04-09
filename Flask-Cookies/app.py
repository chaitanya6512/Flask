# Flask Cookies
from flask import Flask, request, make_response

app = Flask(__name__)

# Using set_cookie() method to set the key-value apirs below.
@app.route('/setcookie')
def setcookie():
    # Initializing response object
    resp = make_response('Setting the Cookie')
    resp.set_cookie('GFG', 'ComputerScience Portal')
    return resp

# Using cookies.get() method - getting cookie from the previous set_cookie code
@app.route('/getcookie')
def getcookie():
    GFG = request.cookies.get('GFG')
    return 'GFG is a'+ GFG

app.run()