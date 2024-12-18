from transector import Transector

if __name__ == "__main__":
    transector = Transector()

    ingredients = transector.get_all_ingredients()
    print("All Ingredients:", ingredients[:10])

    foods = transector.get_all_foods()
    print("All Foods:", foods[:10])

    food_name = "nam prik pla too"
    ingredients_for_food = transector.get_ingredients_for_food(food_name)
    print(f"Ingredients for {food_name}:", ingredients_for_food)

    ingredient_name = "egg"
    foods_with_ingredient = transector.get_foods_for_ingredient(ingredient_name)
    print(f"Foods with {ingredient_name}:", foods_with_ingredient)

    ingredient_synonyms = transector.get_synonym_ingredients(ingredient_name)
    print(f"Synonyms for {ingredient_name}:", ingredient_synonyms)

    transector.close()