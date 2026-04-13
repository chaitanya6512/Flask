from flask import Flask, jsonify, request
from tortoise import Tortoise, fields
from tortoise.models import Model
import asyncio

app = Flask(__name__)

# Define an asynchronous User model
class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(50)
    email = fields.CharField(100, unique=True)

# Initialize Tortoise ORM properly
async def init_tortoise():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",  # Database connection
        modules={"models": ["__main__"]}  # Register models
    )
    await Tortoise.generate_schemas()  # Create tables

@app.before_request
def initialize():
    """Ensure Tortoise ORM is initialized before handling any request."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(init_tortoise())

# Asynchronous route to create a new user
@app.route('/add-user', methods=['POST'])
async def add_user():
    data = request.get_json()  # No await here

    # If using Tortoise ORM (which is async)
    user = await User.create(name=data['name'], email=data['email'])  # Use await on async functions

    return jsonify({"message": "User created", "user": {"id": user.id, "name": user.name, "email": user.email}})

# Asynchronous route to fetch a user by ID
@app.route('/user/<int:user_id>')
async def get_user(user_id):
    user = await User.get_or_none(id=user_id)
    if user:
        return jsonify({"id": user.id, "name": user.name, "email": user.email})
    return jsonify({"error": "User not found"}), 404

# Asynchronous route to fetch all users
@app.route('/users')
async def get_users():
    users = await User.all().values("id", "name", "email")  # Fetch all users asynchronously
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)