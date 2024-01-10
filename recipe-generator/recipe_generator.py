import json
import argparse

from search import search_in_products, search_in_removal_list, search_in_recipe_db
from recipe_llm_helper import generate_recipe
from recipe_constants import DEFAULT_NUMBER_OF_SERVINGS

def remove_listed_items(recipe):
    recipe["ingredients"] = [ingredient for ingredient in recipe["ingredients"] if not search_in_removal_list(ingredient["name"])]
    return recipe

def add_product_ids(recipe):
    for ingredient in recipe["ingredients"]:
        if product := search_in_products(ingredient["name"]):
            ingredient["product_name"] = product[0]
            ingredient["id"] = product[1]
    return recipe

def adjust_ingredient_quantity(recipe, servings):
    servings_in_recipe = int(recipe["servings"])
    adjust_ratio = servings/servings_in_recipe
    for ingredient in recipe["ingredients"]:
        ingredient["quantity"] = str(float(ingredient["quantity"])*adjust_ratio)
    return recipe

def get_recipe(dish_name, servings=DEFAULT_NUMBER_OF_SERVINGS):
    if db_entry := search_in_recipe_db(dish_name):
        recipe = adjust_ingredient_quantity(db_entry, servings)
    else:
        recipe = json.loads(generate_recipe(dish_name, servings))
    recipe = remove_listed_items(recipe)
    recipe_with_product_ids = add_product_ids(recipe)
    return recipe_with_product_ids

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dish_name", help="name of the dish you want the ingredients for")
    parser.add_argument("-s", "--servings", help="number of servings you want", type=int)
    args = parser.parse_args()
    servings = DEFAULT_NUMBER_OF_SERVINGS if args.servings is None else args.servings

    print( get_recipe(args.dish_name, servings) )