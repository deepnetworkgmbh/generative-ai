import json
from pathlib import Path

from openai import AzureOpenAI

import logging_helper
from azure_speech_helper import create_speech_recognizer
from embeddings import Embeddings
from recipe_constants import *
from recipe_generator import RecipeGenerator
from recipe_llm_helper import RecipeLlmHelper
from search import Search
from user_input_handler import UserInputHandler
from user_input_llm_helper import UserInputLlmHelper, UserInputType

IMPORTANT_INFORMATION = """
- Dietary restrictions or preferences, eg. being vegetarian, having allergies
- Style of cooking, eg. baked, fried
- Preferred cuisines, eg. Italian, French
"""

SYSTEM_MESSAGE = """
You are a cooking assistant that will help with finding dishes the user can cook.
Never answer questions unrelated to this task. Instead tell the user "I am a cooking assistant, I cannot help with that"
You have the list of ingredients user has at home below.
Ingredients:
{ingredients}

Assume user has nothing else at home, so try to come up with dishes from the list above.
You can use other ingredients as well but try to keep those to a minimum.
When you come up with a dish, list what ingredients the user will need to buy for that dish.
You will ask questions one by one to come up with a dish that the user will like.
Below are some of the important information you should ask about to the user but if you need other information ask about them as well.
IMPORTANT_INFORMATION:
{important_information}
"""

DISH_SYSTEM_MESSAGE = """
You are a chat analyzer tool, your job is to find the dish user agreed upon in the below chat history.
You must only answer with the dish name and nothing else.
If the user has not picked any dish respond with 'no_dish_chosen'
Chat History:
{chat_history}
"""


def get_ingredients_at_home():
    with open(INGREDIENTS_AT_HOME) as file:
        return json.load(file)


def add_to_messages(history, completion, prompt):
    history.append({"role": "assistant", "content": completion})
    history.append({"role": "user", "content": prompt})
    return history


def chat_with_gpt(client, messages):
    return client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_GPT_DEPLOYMENT"),
        messages=messages,
        temperature=0.7,
        frequency_penalty=0.3
    ).choices[0].message.content


def get_dish_name_from_chat(client, history):
    return client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_GPT_DEPLOYMENT"),
        messages=[{"role": "system", "content": DISH_SYSTEM_MESSAGE.format(chat_history=history)}],
        temperature=0,
    ).choices[0].message.content


def print_missing_ingredients(recipe):
    print("Missing ingredients:")
    for ingredient in recipe["ingredients"]:
        print(f"- {ingredient['name']} -- {ingredient['quantity']} {ingredient['unit']}")


def print_ingredients_at_home():
    print("Ingredients at home:")
    for ingredient in get_ingredients_at_home():
        print(f"- {ingredient}")


def find_recipe_using_ingredients(ingredients, user_input_handler, recipe_gen, client):
    system_message = SYSTEM_MESSAGE.format(ingredients=ingredients, important_information=IMPORTANT_INFORMATION)
    messages = [{"role": "system", "content": system_message}]
    print('You can type "yes" to choose a dish or "exit" to stop the program.')
    while True:
        completion = chat_with_gpt(client, messages)
        prompt = input(f"{completion}\n")
        if prompt == "yes":
            messages = add_to_messages(messages, completion, prompt)
            dish_name = get_dish_name_from_chat(client, messages[1:])
            if dish_name == "no_dish_chosen":
                print("No dish was chosen")
                return None
            else:
                servings = input("For how many servings?\n")
                servings = user_input_handler.clean_input(servings, UserInputType.SERVINGS, None)
                recipe = recipe_gen.get_recipe(dish_name, servings)
                return recipe
        elif prompt == "exit":
            return None
        else:
            messages = add_to_messages(messages, completion, f"My answer to your question: {prompt}")


def remove_ingredients_at_home(recipe):
    recipe["ingredients"] = [ingredient for ingredient in recipe["ingredients"] if
                             not recipe_gen.search.search_in_ingredients_at_home(ingredient["name"])]
    return recipe


if __name__ == "__main__":
    logging_helper.setup_logging(f'{Path(__file__).stem}.log')

    client = AzureOpenAI(
        api_version="2023-09-01-preview"
    )
    azure_openai_model_name = os.getenv('AZURE_OPENAI_GPT_DEPLOYMENT')
    embeddings = Embeddings()
    embeddings.embed_ingredients_at_home()
    search = Search(embeddings)

    recipe_llm_helper = RecipeLlmHelper(client, azure_openai_model_name)
    recipe_gen = RecipeGenerator(search, recipe_llm_helper)

    speech_recognizer = create_speech_recognizer()
    user_input_llm_helper = UserInputLlmHelper(client, azure_openai_model_name)
    user_input_handler = UserInputHandler(user_input_llm_helper, speech_recognizer)

    print_ingredients_at_home()
    ingredients = get_ingredients_at_home()
    recipe = find_recipe_using_ingredients(ingredients, user_input_handler, recipe_gen, client)
    recipe = remove_ingredients_at_home(recipe)
    print_missing_ingredients(recipe)
