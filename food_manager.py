import numpy as np
import json

class FoodManager:
    def __init__(self, users, foods, islam_users, matrix):
        self.users = users
        self.foods = foods
        self.islam_users = set(islam_users)
        self.matrix = np.array(matrix, dtype=int)

    def add_or_update_user(self, user, food_preferences):
        if user not in self.users:
            self.users.append(user)
            new_row = np.zeros(len(self.foods), dtype=int)
            self.matrix = np.vstack([self.matrix, new_row])

        user_index = self.users.index(user)
        for food, preference in food_preferences.items():
            if food in self.foods:
                food_index = self.foods.index(food)
                self.matrix[user_index, food_index] = preference

    def save_to_json(self, filename):
        data = {
            "users": self.users,
            "foods": self.foods,
            "islam_users": list(self.islam_users),
            "matrix": [[int(value) for value in row] for row in self.matrix]
        }
        with open(filename, "w") as file:
            json.dump(data, file)

    @classmethod
    def load_from_json(cls, filename):
        with open(filename, "r") as file:
            data = json.load(file)
        return cls(data["users"], data["foods"], data["islam_users"], data["matrix"])

    def get_user_preferences(self, user):
        print(user)
        if user not in self.users:
            return None
        user_index = self.users.index(user)
        return {self.foods[i]: self.matrix[user_index, i] for i in range(len(self.foods))}

    def is_islam_compliant(self, user):
        return user in self.islam_users if user in self.users else None
