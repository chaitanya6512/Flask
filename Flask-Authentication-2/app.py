# Import all functions/classes from Flask
from flask import *  
# Import Flask-MySQLdb extension to interact with MySQL
from flask_mysqldb import MySQL  
# Import cursor handling for MySQL queries
import MySQLdb.cursors  
# Import regular expressions module for validating email
import re  

# -------------------------------
# Flask App Initialization
# -------------------------------
app = Flask(__name__)  # Create a Flask app instance
app.secret_key = 'GeeksForGeeks'  # Secret key for session management

# -------------------------------
# MySQL Database Configuration
# -------------------------------
app.config['MYSQL_HOST'] = 'localhost'   # Database host
app.config['MYSQL_USER'] = 'root'        # MySQL username
app.config['MYSQL_PASSWORD'] = 'superuser'   # MySQL password (replace with yours)
app.config['MYSQL_DB'] = 'user_table'    # Database name

mysql = MySQL(app)  # Initialize MySQL with Flask app

# -------------------------------
# Function to create 'user' table if not exists
# -------------------------------
def create_table():
    cursor = mysql.connection.cursor()  # Get a cursor to execute SQL queries
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            userid INT AUTO_INCREMENT PRIMARY KEY,  # Unique user ID
            name VARCHAR(100) NOT NULL,            # User's name
            email VARCHAR(100) NOT NULL UNIQUE,    # User's email, must be unique
            password VARCHAR(255) NOT NULL         # User's password
        )
    """)
    mysql.connection.commit()  # Commit changes to the database
    cursor.close()             # Close cursor to free resources

# Call the function when the app starts
with app.app_context():
    create_table()  # Ensure the table exists before handling requests

# -------------------------------
# Login Route
# -------------------------------
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''  # Initialize message for feedback
    # Check if form is submitted and required fields are present
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']        # Get email from form
        password = request.form['password']  # Get password from form
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)  # DictCursor returns dicts
        # Execute SQL query to find user with matching email and password
        cursor.execute(
            'SELECT * FROM user WHERE email = % s AND password = % s', 
            (email, password, )
        )
        user = cursor.fetchone()  # Fetch one result
        if user:  # If user exists
            # Set session variables
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            message = 'Logged in successfully !'
            return render_template('user.html', message=message)  # Render user page
        else:
            message = 'Please enter correct email / password !'
    return render_template('login.html', message=message)  # Render login page with message

# -------------------------------
# Logout Route
# -------------------------------
@app.route('/logout')
def logout():
    # Remove session variables to log out
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))  # Redirect to login page

# -------------------------------
# Registration Route
# -------------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''  # Initialize feedback message
    # Check if form is submitted and required fields exist
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']      # Get name from form
        password = request.form['password']  # Get password from form
        email = request.form['email']        # Get email from form
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Check if account with the same email already exists
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists !'
        # Validate email format using regex
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address !'
        # Check if any field is empty
        elif not userName or not password or not email:
            message = 'Please fill out the form !'
        else:
            # Insert new user into database
            cursor.execute(
                'INSERT INTO user VALUES (NULL, % s, % s, % s)', 
                (userName, email, password, )
            )
            mysql.connection.commit()
            message = 'You have successfully registered !'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    # Render registration page with feedback
    return render_template('register.html', message=message)

# -------------------------------
# Run the Flask App
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)  # Run in debug mode for development