import json
import argparse
import os
from pprint import pprint
from pathlib import Path

from openai.lib.azure import AzureOpenAI

from search import Search
from embeddings import Embeddings
from recipe_llm_helper import RecipeLlmHelper
from recipe_constants import DEFAULT_NUMBER_OF_SERVINGS
import logging_helper


class RecipeGenerator:
    def __init__(self, search: Search, recipe_llm_helper: RecipeLlmHelper):
        self.search = search
        self.recipe_llm_helper = recipe_llm_helper

    def remove_listed_items(self, recipe: dict) -> dict:
        recipe["ingredients"] = [ingredient for ingredient in recipe["ingredients"] if
                                 not self.search.search_in_removal_list(ingredient["name"])]
        return recipe

    def add_product_ids(self, recipe: dict) -> dict:
        for ingredient in recipe["ingredients"]:
            if product := self.search.search_in_products(ingredient["name"]):
                ingredient["product_name"] = product[0]
                ingredient["id"] = product[1]
        return recipe

    def get_recipe(self, dish_name: str, servings: int = DEFAULT_NUMBER_OF_SERVINGS) -> dict:
        if db_entry := self.search.search_in_recipe_db(dish_name):
            recipe = _adjust_ingredient_quantity(db_entry, servings)
        else:
            response = self.recipe_llm_helper.generate_recipe(dish_name, servings)
            recipe = json.loads(response.choices[0].message.content)
        recipe = self.remove_listed_items(recipe)
        recipe = self.add_product_ids(recipe)
        return recipe


def _adjust_ingredient_quantity(recipe: dict, servings: int) -> dict:
    servings_in_recipe = int(recipe["servings"])
    adjust_ratio = servings / servings_in_recipe
    for ingredient in recipe["ingredients"]:
        ingredient["quantity"] = str(float(ingredient["quantity"]) * adjust_ratio)
    recipe["servings"] = servings
    return recipe


if __name__ == "__main__":
    logging_helper.setup_logging(f'{Path(__file__).stem}.log')

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
    recipe = recipe_gen.get_recipe(args.dish_name, servings)

    print("Recipe is:")
    pprint(recipe)
