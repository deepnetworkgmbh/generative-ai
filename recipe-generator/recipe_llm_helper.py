from openai import AzureOpenAI

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
    Always give ingredient names in English even if the dish name is in another language.
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
    }"""}
]


def format_prompt(dish_name, servings):
    return PROMPT_TEMPLATE.format(dish_name=dish_name, servings=servings)


class RecipeLlmHelper:
    def __init__(self, azure_openai_client:AzureOpenAI, azure_openai_model:str):
        self.azure_openai_model = azure_openai_model
        self.azure_openai_client = azure_openai_client

    def generate_recipe(self, dish_name, servings):
        prompt = format_prompt(dish_name, servings)
        return self.generate_completion(prompt).choices[0].message.content

    def generate_completion(self, prompt):
        return self.azure_openai_client.chat.completions.create(
            model=self.azure_openai_model,
            messages=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                *FEW_SHOTS,
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            top_p=0.2,
        )
