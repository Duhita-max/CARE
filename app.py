from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Connect Flask to MongoDB
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)

db = client["care_db"]  # Your database name

# ✅ GET request: Fetch all users (Works in browser)
@app.route('/get_users', methods=['GET'])
def get_users():
    users = list(db.users.find({}, {"_id": 0}))  # Fetch users from MongoDB
    return jsonify(users)

# ✅ POST request: Add a new user (Use Postman or cURL)
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Name and Email are required!"}), 400
    db.users.insert_one(data)
    return jsonify({"message": "User added successfully!"}), 201

# ✅ PUT request: Update a user's name using email
@app.route('/update_user', methods=['PUT'])
def update_user():
    data = request.json
    email = data.get("email")  # Find user by email
    new_name = data.get("name")  # New name to update

    if not email or not new_name:
        return jsonify({"error": "Email and new name are required"}), 400

    result = db.users.update_one({"email": email}, {"$set": {"name": new_name}})
    
    if result.matched_count == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User updated successfully!"})

# ✅ DELETE request: Remove a user by email
@app.route('/delete_user', methods=['DELETE'])
def delete_user():
    data = request.json
    email = data.get("email")  # Find user by email

    if not email:
        return jsonify({"error": "Email is required"}), 400

    result = db.users.delete_one({"email": email})

    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted successfully!"})

# ✅ GET request: Find a specific user by email
@app.route('/find_user/<email>', methods=['GET'])
def find_user(email):
    user = db.users.find_one({"email": email}, {"_id": 0})  # Find user by email
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

if __name__ == '__main__':
    app.run(debug=True)











