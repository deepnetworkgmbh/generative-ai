import json
import os

from openai.lib.azure import AzureOpenAI

from recipe_constants import DEFAULT_NUMBER_OF_SERVINGS
from recipe_constants import RECIPE_DB_PATH
from recipe_llm_helper import RecipeLlmHelper

if __name__ == "__main__":
    azure_openai_model_name = os.getenv('AZURE_OPENAI_GPT_DEPLOYMENT')
    azure_openai = AzureOpenAI(api_version="2023-09-01-preview")

    EXISTING_RECIPE_DB_PATH = f"{os.path.dirname(os.path.abspath(__file__))}/data/existing-recipes-db.json"
    NUMBER_OF_RECIPES = 10

    recipe_names = []

    recipe_llm_helper = RecipeLlmHelper(azure_openai, azure_openai_model_name)

    with open(EXISTING_RECIPE_DB_PATH, 'r') as file:
        db = json.load(file)
        for recipe in db.values():
            recipe_names.append(recipe["name"])

    new_recipe_db = []

    for recipe_name in recipe_names[:NUMBER_OF_RECIPES]:
        new_recipe_db.append(json.loads(recipe_llm_helper.generate_recipe(recipe_name, DEFAULT_NUMBER_OF_SERVINGS).choices[0].message.content))

    with open(RECIPE_DB_PATH, 'w') as file:
        json.dump(new_recipe_db, file)
