from flask import Flask, request, jsonify
from uuid import uuid4
from datetime import datetime

app = Flask(__name__)

# In-memory database
users = {}

# Helper function to format responses
def make_response(status, message, data=None):
    return jsonify({
        "status": status,
        "message": message,
        "data": data
    })

# GET - All users
@app.route('/users', methods=['GET'])
def get_users():
    return make_response("success", "All users fetched", users)

# GET - Single user by UUID
@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return make_response("success", "User found", {user_id: user})
    return make_response("error", "User not found"), 404

# GET - Search users by name
@app.route('/users/search', methods=['GET'])
def search_users():
    name_query = request.args.get("name", "").lower()
    results = {uid: info for uid, info in users.items() if name_query in info["name"].lower()}
    return make_response("success", "Search results", results)

# POST - Create user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or "name" not in data:
        return make_response("error", "Name is required"), 400
    uid = str(uuid4())
    users[uid] = {
        "name": data["name"],
        "email": data.get("email", ""),
        "created_at": datetime.now().isoformat(),
        "updated_at": None
    }
    return make_response("success", "User created", {uid: users[uid]}), 201

# PUT - Update user
@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return make_response("error", "User not found"), 404
    data = request.get_json()
    user.update(data)
    user["updated_at"] = datetime.now().isoformat()
    return make_response("success", "User updated", {user_id: user})

# DELETE - Remove user
@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        deleted = users.pop(user_id)
        return make_response("success", "User deleted", {user_id: deleted})
    return make_response("error", "User not found"), 404

if __name__ == '__main__':
    app.run(debug=True)
