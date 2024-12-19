from flask import Flask, jsonify, request
from flask_cors import CORS
from recommend import popularity, CF, CB
from allergy import food_to_allergy, ingredient_to_allergy
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Food Recommendation API!"})

# Popularity-based Recommendation Endpoint
@app.route('/recommend/popularity', methods=['GET'])
def recommend_popularity():
    try:
        result = popularity()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Collaborative Filtering Recommendation Endpoint
@app.route('/recommend/cf', methods=['POST'])
def recommend_cf():
    try:
        data = request.json
        if not data or 'food_name' not in data:
            return jsonify({"error": "Please provide 'food_name' in the request body"}), 400

        food_name = data['food_name']
        result = CF(food_name)
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": f"Invalid input: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Content-Based Recommendation Endpoint
@app.route('/recommend/cb', methods=['GET'])
def recommend_cb():
    try:
        result = CB()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/allergy/food', method=['POST'])
def allergy_food():
    try:
        data = request.json
        if not data or 'food_name' not in data:
            return jsonify({"error": "Please provide 'food_name' in the request body"}), 400
        
        food_name = data['food_name']
        result = food_to_allergy(food_name)
        return jsonify({"allergy": result}), 200
    except ValueError as ve:
        return jsonify({"error": f"Invalid input: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/allergy/ingredient', method=['POST'])
def allergy_ingredient():
    try:
        data = request.json
        if not data or 'ingredients' not in data:
            return jsonify({"error": "Please provide 'ingredients' in the request body"}), 400
        
        ingredients = data['ingredients']
        result = ingredient_to_allergy(ingredients)
        return jsonify({"allergy": result}), 200
    except ValueError as ve:
        return jsonify({"error": f"Invalid input: {str(ve)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Route not found"}), 404

@app.teardown_appcontext
def teardown_appcontext(exception):
    if exception:
        print(f"Teardown exception: {exception}")

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, port=port)
