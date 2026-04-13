# Flask requires a SERVER_NAME setting for subdomains to work. 
# This includes both the domain name and the port number.

from flask import Flask

app = Flask(__name__)
app.config['SERVER_NAME'] = 'vibhu.gfg:5000'

@app.route('/')
def home():
    return "Welcome to GeeksForGeeks !"

if __name__ == "__main__":
    app.run()