import json
from recipe_generator import generate_recipe
from recipe_constants import DEFAULT_NUMBER_OF_SERVINGS
from recipe_constants import RECIPE_DB_PATH

EXISTING_RECIPE_DB_PATH = "./recipe_generator/data/existing-recipes-db.json"
NUMBER_OF_RECIPES = 10

recipe_names = []

with open(EXISTING_RECIPE_DB_PATH, 'r') as file:
    db = json.load(file)
    for recipe in db.values():
        recipe_names.append(recipe["name"])

new_recipe_db = []

for recipe_name in recipe_names[:NUMBER_OF_RECIPES]:
    new_recipe_db.append(json.loads(generate_recipe(recipe_name, DEFAULT_NUMBER_OF_SERVINGS)))

with open(RECIPE_DB_PATH, 'w') as file:
    json.dump(new_recipe_db, file)