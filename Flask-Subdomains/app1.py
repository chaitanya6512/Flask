# Creating Multiple Endpoints with Subdomains

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to GeeksForGeeks !"

@app.route('/basic/')
def basic():
    return "Basic Category Articles listed on this page."

@app.route('/', subdomain='practice')
def practice():
    return "Coding Practice Page"

@app.route('/courses/', subdomain='practice')
def courses():
    return "Courses listed under practice subdomain."

if __name__ == "__main__":
    website_url = 'vibhu.gfg:5000'
    app.config['SERVER_NAME'] = website_url
    app.run()