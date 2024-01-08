import json

from ingredient_finder import search_in_products
from recipe_generator import generate_recipe, DEFAULT_NUMBER_OF_SERVINGS

def check_recipe_db(dish_name):
    with open(f"./recipe-generator/new-recipe-db.json", 'r') as file:
        db = json.load(file)
        for recipe in db:
            if recipe["name"] == dish_name:
                return recipe
    return None

def remove_listed_items(removal_list_file, recipe):
    pass

def main(dish_name, servings):
    recipe = {}
    if db_entry := check_recipe_db(dish_name):
        recipe = db_entry
    else:
        recipe = generate_recipe(dish_name, servings)
    
    recipe = remove_listed_items("")

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dish_name", help="name of the dish you want the ingredients for")
    parser.add_argument("-s", "--servings", help="number of servings you want", type=int)
    args = parser.parse_args()
    dish_name = args.dish_name
    servings = DEFAULT_NUMBER_OF_SERVINGS if args.servings is None else args.servings

    main(dish_name, servings)