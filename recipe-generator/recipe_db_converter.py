import json
import recipe_generator

recipe_names = []

with open(f"./recipe-generator/db-recipes.json", 'r') as file:
    db = json.load(file)
    for recipe in db.values():
        recipe_names.append(recipe["name"])

new_recipe_db = []

for recipe_name in recipe_names[:3]:
    new_recipe_db.append(json.loads(recipe_generator.generate_recipe(recipe_name,4)))

with open(f"./recipe-generator/new-recipe-db.json", 'w') as file:
    json.dump(new_recipe_db, file)