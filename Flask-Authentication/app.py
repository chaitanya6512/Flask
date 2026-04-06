# Import Required Libraries and Extensions
from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# Create a Flask application instance
app = Flask(__name__)

# Configuration the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"   # Database file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    # Disable modification tracking(Saves memory)
app.config["SECRET_KEY"] = "supersecretkey"     # Secret key for sessions(Should kept secure)

# Initialize database object with app
db = SQLAlchemy(app)

# Initialize Flask-Login manager
login_manager = LoginManager()
login_manager.init_app(app)  # Attach login manager to app
login_manager.login_view = "login"  # Redirect to 'login' if user not logged in 

# Define User model(table structure)
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)    # Unique ID for each user
    username = db.Column(db.String(250), unique=True, nullable=False)   # Username(must be unqiue)
    password = db.Column(db.String(250), nullable=False)     # Hashable password

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Function to load a user by ID (required by Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))    # Fetch user from DB

# Home page route
@app.route("/")
def home():
    return render_template("home.html")     # Render home page

# User registration route
@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if username already exists
        if Users.query.filter_by(username=username).first():
            return render_template('sign_up.html', error="Username already taken")
        
        # Hash the password for security
        hashed_passowrd = generate_password_hash(password, method="pbkdf2:sha256")

        # Create new user object
        new_user = Users(username=username, password=hashed_passowrd)

        # Save user to database
        db.session.add(new_user)
        db.session.commit()

        # Redirect to login page after successful regirstration
        return redirect(url_for('login'))
        
    return render_template('sign_up.html')
    
# User login route
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # Get login credentials from form
        username = request.form.get('username')
        password = request.form.get('password')

        # Find user in database
        user = Users.query.filter_by(username=username).first()

        # Verify Password
        if user and check_password_hash(user.password, password):
            login_user(user)    # Log the user in
            return redirect(url_for("dashboard"))   # Redirect to dashboard
        else:
            return render_template('login.html', error="Invalid username or password")
            
    # If GET request, show login form
    return render_template('login.html')

# Protected route (only accessible if logged in)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()   # Log the user out
    return redirect(url_for('home'))    # Redirect to home page

# Run the app in debug mode
if __name__ == "__main__":
    app.run(debug=True)     # Debug=True enables auto-related and error messages
        

