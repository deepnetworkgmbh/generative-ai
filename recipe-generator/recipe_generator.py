import json
import argparse
import os

from openai.lib.azure import AzureOpenAI

from search import Search
from embeddings import Embeddings
from recipe_llm_helper import RecipeLlmHelper
from recipe_constants import DEFAULT_NUMBER_OF_SERVINGS


class RecipeGenerator:
    def __init__(self, search: Search, recipe_llm_helper: RecipeLlmHelper):
        self.search = search
        self.recipe_llm_helper = recipe_llm_helper

    def remove_listed_items(self, recipe):
        recipe["ingredients"] = [ingredient for ingredient in recipe["ingredients"] if
                                 not self.search.search_in_removal_list(ingredient["name"])]
        return recipe

    def add_product_ids(self, recipe):
        for ingredient in recipe["ingredients"]:
            if product := self.search.search_in_products(ingredient["name"]):
                ingredient["product_name"] = product[0]
                ingredient["id"] = product[1]
        return recipe

    def get_recipe(self, dish_name, servings=DEFAULT_NUMBER_OF_SERVINGS):
        if db_entry := self.search.search_in_recipe_db(dish_name):
            recipe = _adjust_ingredient_quantity(db_entry, servings)
        else:
            recipe = json.loads(self.recipe_llm_helper.generate_recipe(dish_name, servings))
        recipe = self.remove_listed_items(recipe)
        recipe_with_product_ids = self.add_product_ids(recipe)
        return recipe_with_product_ids


def _adjust_ingredient_quantity(recipe, servings):
    servings_in_recipe = int(recipe["servings"])
    adjust_ratio = servings / servings_in_recipe
    for ingredient in recipe["ingredients"]:
        ingredient["quantity"] = str(float(ingredient["quantity"]) * adjust_ratio)
    recipe["servings"] = servings
    return recipe


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dish_name", help="name of the dish you want the ingredients for")
    parser.add_argument("-s", "--servings", help="number of servings you want", type=int)
    args = parser.parse_args()
    servings = DEFAULT_NUMBER_OF_SERVINGS if args.servings is None else args.servings

    embeddings = Embeddings()
    search = Search(embeddings)
    azure_openai = AzureOpenAI(api_version="2023-09-01-preview")
    azure_openai_model_name = os.getenv('AZURE_OPENAI_GPT_DEPLOYMENT')

    recipe_llm_helper = RecipeLlmHelper(azure_openai, azure_openai_model_name)
    recipe_gen = RecipeGenerator(search, recipe_llm_helper)
    print(recipe_gen.get_recipe(args.dish_name, servings))
