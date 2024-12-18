from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from food_manager import FoodManager

app = Flask(__name__)
CORS(app)

DATA_FILE = "mock_data/matrix.json"

if os.path.exists(DATA_FILE):
    food_manager = FoodManager.load_from_json(DATA_FILE)
else:
    food_manager = FoodManager(
        users=[], foods=[], islam_users=[], matrix=[]
    )

@app.route('/user/<string:user>', methods=['GET'])
def get_user_preferences(user):
    preferences = food_manager.get_user_preferences(user)
    if preferences is None:
        return jsonify({"error": "User not found"}), 404
    
    preferences = {food: int(value) for food, value in preferences.items()}
    return jsonify({"user": user, "preferences": preferences})

@app.route('/user', methods=['POST'])
def add_or_update_user():
    data = request.json
    user = data.get("user")
    food_preferences = data.get("preferences", {})
    if not user:
        return jsonify({"error": "User is required"}), 400

    food_manager.add_or_update_user(user, food_preferences)
    food_manager.save_to_json(DATA_FILE)
    return jsonify({"message": f"User {user} added/updated successfully"})

@app.route('/')
def index():
    return "Hello"

@app.teardown_appcontext
def save_data_on_teardown(exception):
    food_manager.save_to_json(DATA_FILE)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))