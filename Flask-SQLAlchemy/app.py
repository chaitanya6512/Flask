from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids a warning

# Create SQLAlchemy Database
db = SQLAlchemy(app)

# In sqlalchemy, we use classes to create our database structure.
# We will create a Profile table that will be responsible for holding the user's id, first name, last name, and age
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Name:{self.first_name}, Age:{self.age}"

# Function to render index page
@app.route('/')
def index():
    profiles = Profile.query.all()
    return render_template('index.html', profiles=profiles)

@app.route('/add_data')
def add_data():
    return render_template('add_profile.html')

# Function to add profiles
@app.route('/add', methods=['POST'])
def profile():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    age = request.form.get("age")

    if first_name != '' and last_name != '' and age is not None:
        p = Profile(first_name=first_name, last_name=last_name, age=age)
        db.session.add(p)
        db.session.commit()
        return redirect('/')
    return redirect('/')
    
@app.route('/delete/<int:id>')
def erase(id):
    # Deletes the data on the basis of unqiue id and 
    # Redirects to Home Page
    data = Profile.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')


# Run the app and create database
if __name__ == '__main__':
    with app.app_context():     # Needed for DB operations
        db.create_all()         # Creates the database and tables
    app.run(debug=True)