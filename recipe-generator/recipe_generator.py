import os
import json
import argparse
from openai import AzureOpenAI

DEFAULT_NUMBER_OF_SERVINGS = 4

JSON_SCHEMA = {
    "name": "[RECIPE_NAME]",
    "servings": "[NUMBER_OF_SERVINGS]",
    "ingredients": [
        {
            "name": "[INGREDIENT_NAME]",
            "quantity": "[NUMERIC_QUANTITY]",
            "unit": "[UNIT_OF_MEASUREMENT]"
        }
    ]
}

SYSTEM_MESSAGE = """
    You are a cooking assistant that will help generate a list of ingredients for any dish user asks for.
    You will consider the number of servings when deciding on the quantities of ingredients.
    First generate the ingredient list; then if the list has any non-metric units such as teaspoon, tablespoon or cup, you must convert them to metric units such as gram or liter.
    You must give the ingredient name and unit in singular form such as egg, tomato, gram or liter.
    Always use gram as the measurement "unit" for fruits and vegetables.
    Do not use fractions as quantities, instead use decimals.
    Do not give descriptors on how to prepare the ingredient in the name field.
    You must give the list of ingredients using the following JSON schema.
    JSON schema:
    {json_schema}
""".format(json_schema=JSON_SCHEMA)


PROMPT_TEMPLATE = """
    Give me the list of ingredients for {dish_name} for {servings} servings.
"""

FEW_SHOTS = [
    {"role": "user", "content": "Give me the list of ingredients for Vanilla cake for 8 servings."},
    {"role": "assistant", "content": """{
        "name": "Vanilla Cake",
        "servings": "8",
        "ingredients": [
            {"name": "All purpose flour", "quantity": "315", "unit": "gram"},
            {"name": "Butter", "quantity": "460", "unit": "gram"},
            {"name": "Granulated sugar", "quantity": "250", "unit": "gram"},
            {"name": "Baking powder", "quantity": "12", "unit": "gram"},
            {"name": "Egg", "quantity": "3", "unit": "pieces"},
            {"name": "Vanilla extract", "quantity": "10", "unit": "milliliter"},
            {"name": "Salt", "quantity": "1.5", "unit": "grams"},
            {"name": "Whole milk", "quantity": "280", "unit": "milliliter"},
            {"name": "Yogurt", "quantity": "60", "unit": "milliliter"},
            {"name": "Powdered sugar", "quantity": "500", "unit": "gram"}
        ]
    }""" }
]

def write_to_file(dish_name, completion):
    with open(f"./recipe-generator/recipes/{dish_name}-ingredients.json".lower().replace(" ","-"), 'w') as file:
        file.write(completion)

def format_prompt(dish_name, servings):
    return PROMPT_TEMPLATE.format(dish_name=dish_name, servings=servings)

def generate_completion(client, prompt):
    return client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_GPT_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            *FEW_SHOTS,
            {"role": "user", "content": prompt},
        ],
        response_format={ "type": "json_object" },
        top_p=0.2,
    )

def generate_recipe(dish_name, servings):
    client = AzureOpenAI(
        api_version="2023-09-01-preview"
    )
    prompt = format_prompt(dish_name, servings)
    return generate_completion(client, prompt).choices[0].message.content

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dish_name", help="name of the dish you want the ingredients for")
    parser.add_argument("-s", "--servings", help="number of servings you want", type=int)
    args = parser.parse_args()
    dish_name = args.dish_name
    servings = DEFAULT_NUMBER_OF_SERVINGS if args.servings is None else args.servings

    completion = generate_recipe(dish_name, servings)
    write_to_file(dish_name, completion)
