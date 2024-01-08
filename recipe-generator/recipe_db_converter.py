import json
from recipe_generator import generate_recipe, DEFAULT_NUMBER_OF_SERVINGS

recipe_names = []

with open(f"./recipe-generator/db-recipes.json", 'r') as file:
    db = json.load(file)
    for recipe in db.values():
        recipe_names.append(recipe["name"])

new_recipe_db = []

for recipe_name in recipe_names[:10]:
    new_recipe_db.append(json.loads(generate_recipe(recipe_name, DEFAULT_NUMBER_OF_SERVINGS)))

with open(f"./recipe-generator/new-recipe-db.json", 'w') as file:
    json.dump(new_recipe_db, file)