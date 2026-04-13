# Import Flask core components
from flask import Flask, render_template, request

# Import Socket.IO features for real-time communication
from flask_socketio import SocketIO, send, emit, join_room, leave_room

# Create a Flask application instance
app = Flask(__name__)

# Secret key is used for sessions and security
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize socket.IO with the Flask app
socketio = SocketIO(app)

# Dictionary to store users and their assigned rooms
# Key = sessions ID (unique per connection)
# Value = username
users = {}

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Event: when a user joins the chat
@socketio.on('join')
def handle_join(username):
    # request.sid = unique session ID for each connected client
    users[request.sid] = username   # Save username mapped to this session

    # Create/join a room named after the user
    # (each user gets their own private room)
    join_room(username)

    # Send a message ONLY to this user's room
    emit("message", f"{username} joined the chat", room=username)

# Event: when a message is sent
@socketio.on('message')
def handle_message(data):
    # Get username using session ID
    # If not found, default to "Anonymous"
    username = users.get(request.sid, "Anonymous")

    # Send message to ALL connected clients
    emit("message", f"{username}:{data}", broadcast=True)

# Event: when a user disconnects
@socketio.on('disconnect')
def handle_disconnect():
    # Remove user from dictionary and get their name
    username = users.pop(request.sid, "Anonymous")

    # Notify everyone that the user left
    emit("messages", f"{username} left the chat", broadcast=True)

# Run the app
if __name__ == "__main__":
    socketio.run(app, debug=True)