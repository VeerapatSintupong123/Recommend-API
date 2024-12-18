import numpy as np
import json
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from transector import Transector
import random

Matrix = np.load('mock_data/Matrix.npy')

with open('mock_data/food.json', 'r') as f:
    food_data = json.load(f)
foods = list(food_data.keys())

with open('mock_data/resturant.json', 'r') as f:
    restaurant_data = json.load(f)

# Best Restaurant Function
def best_restaurant(top_foods):
    top_food_names = []
    for food in top_foods:
        if food in food_data and "English" in food_data[food] and food_data[food]["English"]:
            top_food_names.append(food_data[food]["English"])

    # Calculate restaurant scores
    scores = {}
    for restaurant in restaurant_data.values():
        scores[restaurant["name"]] = 0
        for m in restaurant["menu"]:
            dish = m["dish"]
            if dish in top_food_names:
                scores[restaurant["name"]] += 1

    if not scores:
        return {"error": "No matching restaurants found"}

    best_restaurant_name = max(scores, key=scores.get)
    best_restaurant = None
    for restaurant in restaurant_data.values():
        if restaurant["name"] == best_restaurant_name:
            best_restaurant = {"name": restaurant["name"], "menu": restaurant["menu"]}
            break

    return {"best_restaurant": best_restaurant}

# Popularity-based Recommendation
def popularity():
    temp = [0 for _ in range(len(foods))]
    for j in range(len(foods)):
        for i in range(Matrix.shape[0]):
            temp[j] += Matrix[i][j]

    # Get the top 5 most popular foods
    top_indices = np.argsort(temp)[-5:][::-1]
    top_foods = [foods[i] for i in top_indices]
    return best_restaurant(top_foods)

# Collaborative Filtering (CF) based Recommendation
def CF(food_name):
    index = foods.index(food_name)

    # SVD to make correlation matrix
    SVD = TruncatedSVD(n_components=10)
    decomposed_matrix = SVD.fit_transform(Matrix)
    correlation_matrix = pd.DataFrame(data=decomposed_matrix).corr()

    recommend_list = correlation_matrix[index].to_list()
    score_dict = {foods[i]: score for i, score in enumerate(recommend_list)}

    filtered_scores = {k: v for k, v in score_dict.items() if k != food_name}
    top_foods = [k for k, v in sorted(filtered_scores.items(), key=lambda item: item[1], reverse=True)[:5]]
    return best_restaurant(top_foods)

# Content-Based (CB) Recommendation
def CB():
    transector = Transector()
    number = random.randint(0, 499)
    preference = Matrix[number]
    food_for_person = [foods[i] for i, freq in enumerate(preference) if freq > 0]

    set_ingredient = set()
    for food in food_for_person:
        ingredients = transector.get_ingredients_for_food(food)
        set_ingredient.update(ingredients)

    all_food_scores = {}
    for ingredient in set_ingredient:
        query_foods = transector.get_foods_for_ingredient(ingredient)

        for food in query_foods:
            if food not in food_for_person:
                food_ingredients = transector.get_ingredients_for_food(food)
                common_ingredients = set_ingredient.intersection(food_ingredients)
                similarity_score = len(common_ingredients) / len(set_ingredient.union(food_ingredients))

                if food in all_food_scores:
                    all_food_scores[food] += similarity_score
                else:
                    all_food_scores[food] = similarity_score

    recommended_foods = sorted(all_food_scores.items(), key=lambda x: x[1], reverse=True)
    top_food = [food for food, score in recommended_foods[:5]]
    transector.close()

    return best_restaurant(top_food)