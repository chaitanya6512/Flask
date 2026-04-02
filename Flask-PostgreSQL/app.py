from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Connect to the database
db = psycopg2.connect(database="flask_db", user="postgres",
                      password="superuser", host="localhost", port="5432")

# Create a cursor
cur = db.cursor()

# If you already have any table or not it doesn't matter.
# We will create a Product table for you.
cur.execute(
    '''CREATE TABLE IF NOT EXISTS products(id serial \
        PRIMARY KEY, name varchar(100), price float);'''
)

# Insert some data into the table
cur.execute(
    '''INSERT INTO products(name, price) VALUES \
        ('Apple', 1.99), ('Orange', 0.99), ('Banana', 0.59);'''
)

# commit the changes
db.commit()

# Close the cursor and connection
cur.close()
db.close()


@app.route('/')
def index():
    # Connect to the database
    db = psycopg2.connect(database="flask_db", user="postgres", 
                          password="superuser", host="localhost", port="5432")
    
    # Create a cursor
    cur = db.cursor()

    # Select all products from the table
    cur.execute('''SELECT * FROM products''')

    # Fetch the data
    data = cur.fetchall()

    # Close the cursor and connection
    cur.close()
    db.close()

    return render_template('index.html', data=data)


@app.route('/create', methods=["POST"])
def create():
    # Connect to the database
    db = psycopg2.connect(database="flask_db", user="postgres",
                          password="superuser", host="localhost", port="5432")
    
    # Create a cursor
    cur = db.cursor()

    # Get the data from the form
    name = request.form['name']
    price = request.form['price']

    # Insert the data into the table
    cur.execute(
        '''INSERT INTO products  
        (name, price) VALUES (%s, %s)''',
        (name, price)
    )

    # Commit the changes
    db.commit()

    # Close the cursor and connection
    cur.close()
    db.close()

    return redirect(url_for('index'))


@app.route('/update', methods=["POST"])
def update():
    # Connect to the Database
    db = psycopg2.connect(database="flask_db", user="postgres",
                          password="superuser", host="localhost", port="5432")
    
    # Create a cursor
    cur = db.cursor()

    # Get the data from the form
    name = request.form['name']
    price = request.form['price']
    id = request.form['id']

    # Update the data in the table
    cur.execute(
        ''' UPDATE products SET name=%s,
        price=%s WHERE id=%s''', (name, price, id))
    
    # commit the changes
    db.commit()

    # Close the cursor and connection
    cur.close()
    db.close()

    return redirect(url_for('index'))


@app.route('/delete', methods=["POST"])
def delete():
    # Connect to the Database
    db = psycopg2.connect(database='flask_db', user="postgres",
                          password="superuser", host="localhost", port="5432")
    
    # Create a cursor
    cur = db.cursor()

    # Get the data from the form
    id = request.form['id']

    # Delete the data from the table
    cur.execute(
        '''DELETE FROM products WHERE id=%s''', (id,)
    )

    # commit the changes
    db.commit()

    # Close the cursor and connection
    cur.close()
    db.close()

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
