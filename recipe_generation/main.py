import os
from pathlib import Path
from pprint import pprint

from openai.lib.azure import AzureOpenAI

import logging_helper
from azure_speech_helper import create_speech_recognizer
from embeddings import Embeddings
from recipe_generator import RecipeGenerator
from recipe_llm_helper import RecipeLlmHelper
from search import Search
from user_input_handler import UserInputHandler
from user_input_llm_helper import UserInputLlmHelper

if __name__ == "__main__":
    logging_helper.setup_logging(f'{Path(__file__).stem}.log')

    azure_openai_model_name = os.getenv('AZURE_OPENAI_GPT_DEPLOYMENT')
    azure_openai = AzureOpenAI(api_version="2023-09-01-preview")

    speech_recognizer = create_speech_recognizer()

    user_input_llm_helper = UserInputLlmHelper(azure_openai, azure_openai_model_name)
    user_input_handler = UserInputHandler(user_input_llm_helper, speech_recognizer)

    embeddings = Embeddings()
    search = Search(embeddings)
    recipe_llm_helper = RecipeLlmHelper(azure_openai, azure_openai_model_name)
    recipe_gen = RecipeGenerator(search, recipe_llm_helper)

    dish_name, servings = user_input_handler.get_dish_name_and_servings()
    print(f"Getting recipe of {dish_name} for {servings} servings. ")
    recipe = recipe_gen.get_recipe(dish_name, servings)
    print("Recipe is: ")
    pprint(recipe)
