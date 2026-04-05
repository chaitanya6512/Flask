from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'superuser' # Enter your MySQL Password
app.config['MYSQL_DB'] = 'geeklogin'

mysql = MySQL(app)

# '/' and '/login' both point to this function
@app.route('/')
@app.route('/login', methods=['GET','POST'])
def login():
    # Message to display (error/success)
    msg = ''

    # Check if form is submitted with POST method
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Create cursor (DictCursor returns data as dictionary)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Execute SQL query to check user credentials
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password =%s',
                       (username, password))
        
        account = cursor.fetchone()

        # If account exists  → Login success
        if account:
            session['loggedin'] = True                  # Store Login status
            session['id'] = account['id']               # Store user ID
            session['username'] = account['username']   # Store username

            # Redirect to home page
            return render_template('index.html', msg='Logged in Successfully!')
        else:
            # If no match  → Invalid credentials
            msg = 'Incorrect username/password!'

    # Show login page with message
    return render_template('login.html', msg=msg)   

@app.route('/logout')
def logout():
    #Remove session data(logout user)
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    # Redirect back to login page
    return redirect(url_for('login'))


# Register route
@app.route('/register', methods=['GET','POST'])
def register():
    # Message for feedback
    msg = ''

    # Check if form submitted with required fields
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Get form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Create cursor
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Check if already exists
        cursor.execute('SELECT * FROM accounts WHERE username=%s',(username))
        account = cursor.fetchone()

        # Validations
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):  # Validate email using regex
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):    # Username should be alphanumeric
            msg = 'Username must contain only letters and numbers!'
        elif not username or not password or not email:     #Check empty fields
            msg = 'Please fill out the form'
        else:
            # Insert new user into database
            cursor.execute(
                'INSERT INTO accounts VALUES (NULL, %s, %s, %s)',
                (username, password, email)
            )
            # Save changes
            mysql.connection.commit()

            msg = 'You have successfully registered!'

    return render_template('register.html', msg=msg)

if __name__ == "__main__":
    app.run(debug=True)