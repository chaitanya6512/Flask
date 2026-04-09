# Import required libraries
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt  
import uuid 
from datetime import datetime, timezone, timedelta
from functools import wraps

# Create Flask app instance
app = Flask(__name__)

# ------ Configuration -----
# Secret key used for sessions and JWT encoding
app.config['SECRET_KEY'] = 'ypur_secret_key'

# SQLite database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'

# Disable modification tracking (saves memory)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --------- Database Setup --------
# Initialize database
db = SQLAlchemy(app)

# User model (table in database)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # Primary key
    public_id = db.Column(db.String(50), unique=True)   # Public identifier (UUID)
    name = db.Column(db.String(70), unique=True)    # User name
    email = db.Column(db.String(250), unique=True)  # Unique email
    password = db.Column(db.String(250))    # Hashed password

# ------ AUTH DECORATOR -------
# Decorator to protect routes (requires valid token)
def token_required(f):
    @wraps(f)       # Preserves the original function's name and metadata
    def decorated(*args, **kwargs):
        # Get JWT token from cookies
        token = request.cookies.get('jwt_token')

        # If token is missing → unauthorized
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decode token using secret key
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])

            # Get user from database using public_id
            current_user = User.query.filter_by(public_id=data['public_id']).first()

        except:
            # If token is invalid or expired
            return jsonify({'message': 'Token is invalid!'}), 401

        # Pass current_user to the route
        return f(current_user, *args, **kwargs)
    
    return decorated

# ------- Routes --------
# Home route  → shows Login page
@app.route('/')
def home():
    return render_template('login.html')

# ----- Login ------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        password = request.form['password']

        # Check if user exists
        user = User.query.filter_by(email=email).first()

        # Validate password
        if not user or not check_password_hash(user.password, password):
            return jsonify({'message': 'Invalid email or password!'}), 401
        
        # Create JWT token (valid for 1 hour)
        token = jwt.encode(
            {
                'public_id': user.public_id,
                'exp': datetime.now(timezone.utc) + timedelta(hours=1)
            },
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        # Redirect to dashboard and store token in cookies
        response = make_response(redirect(url_for('dashboard')))
        response.set_cookie('jwt_token', token)

        return response
    
    # If GET request  → show login page
    return render_template('login.html')

# ------- Register / SignUp -------
@app.route('/signup', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # Get user input
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'message':'User already exists. Please login.'}), 400
        
        # Hash password before storing
        hashed_password = generate_password_hash(password)

        # Create new user with UUID
        new_user = User(
            public_id=str(uuid.uuid4()),
            name=name,
            email=email,
            password=hashed_password
        )

        # Save user to database
        db.session.add(new_user)
        db.session.commit()

        # Redirect to login page after signup
        return redirect(url_for('login'))
    
    # If GET request  → show register page
    return render_template('register.html')

# ---- Protected Route ------
@app.route('/dashboard')
@token_required     # Only accessible with valid token
def dashboard(current_user):
    # Current_user comes from token_required decorator
    return f"Welcome {current_user.name}! You are logged in."

# ------- Run Application ----
if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    # Run Flask app in debug mode
    app.run(debug=True)