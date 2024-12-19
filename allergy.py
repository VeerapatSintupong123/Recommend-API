import json

def food_to_allergy(food_name):
    with open('mock_data/food.json', 'r') as f: data = json.load(f)
    foods = list(data.keys())

    with open('mock_data/allergy.json') as f: data2 = json.load(f)
    allergies = list(data2.keys())

    food_to_allergy = {food:[] for food in foods}
    for food in foods:
        ingredients = data[food]["Ingredient"]
        for ingredient in ingredients:
            for allergy in allergies:
                if ingredient in data2[allergy]["Ingredient"]:
                    food_to_allergy[food].append(allergy)

    return food_to_allergy[food_name]

def ingredient_to_allergy(ings):
    with open('mock_data/allergy.json') as f: data2 = json.load(f)
    allergies = list(data2.keys())

    result = []
    for ingredient in ings:
        for allergy in allergies:
            ingredients = data2[allergy]["Ingredient"]
            ingredients = [i.lower() for i in ingredients]
            if ingredient.lower() in ingredients:
                result.append(allergy)

    return result