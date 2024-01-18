import os
import time
import unittest
from openai import AzureOpenAI
from ..recipe_llm_helper import RecipeLlmHelper, format_prompt
import test_helpers

class TestRecipeLlmHelper(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestRecipeLlmHelper, self).__init__(*args, **kwargs)
        # Custom fields
        self.azure_openai_model_name = os.getenv('AZURE_OPENAI_GPT_DEPLOYMENT')
        self.azure_openai_client = AzureOpenAI(api_version="2023-09-01-preview")
        self.recipe_llm_helper = RecipeLlmHelper(self.azure_openai_client, self.azure_openai_model_name)
        self.dish_name_and_numbers_mixed_lang = []

        with open('recipe-generator/test/test_data/dish_name_and_numbers_mixed_lang.txt', 'r') as file:
            for line in file:
                sentence = line.split(" - ")
                self.dish_name_and_numbers_mixed_lang.append([sentence[0].strip(), sentence[1].strip()])

    # TODO: not clear what is being tested. no assertions.
    def test_generate_recipe(self):
        start_time = time.time()
        results = []

        for dish, servings in self.dish_name_and_numbers_mixed_lang:
            response = self.recipe_llm_helper.generate_recipe(dish, servings)
            results.append({
                "completion_tokens": response.usage.completion_tokens,
                "prompt_tokens": response.usage.prompt_tokens
            })

        end_time = time.time()
        test_helpers.calculate_and_print_metrics(
            "Generate Recipe: dish_name_and_numbers_mixed_lang:",
            results,
            end_time - start_time
        )
