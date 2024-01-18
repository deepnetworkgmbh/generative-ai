import os
import json
import time
import unittest
from pathlib import Path

from openai import AzureOpenAI

from recipe_generator.recipe_llm_helper import RecipeLlmHelper
import test_helpers


class TestRecipeLlmHelper(unittest.TestCase):
    dish_name_and_numbers_mixed_lang = []
    test_metrics = []

    @classmethod
    def setUpClass(cls):
        azure_openai_model_name = os.getenv('AZURE_OPENAI_GPT_DEPLOYMENT')
        azure_openai_client = AzureOpenAI(api_version="2023-09-01-preview")
        cls.recipe_llm_helper = RecipeLlmHelper(azure_openai_client, azure_openai_model_name)

        with open('test_data/dish_name_and_numbers_mixed_lang.txt', 'r') as file:
            for line in file:
                sentence = line.split(" - ")
                cls.dish_name_and_numbers_mixed_lang.append([sentence[0].strip(), sentence[1].strip()])

    @classmethod
    def tearDownClass(cls):
        with open(f'{Path(__file__).stem}_results.json', 'w') as file:
            json.dump(cls.test_metrics, file, indent=2)

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
        self.test_metrics.append(
            test_helpers.calculate_metrics(
                "Generate Recipe: dish_name_and_numbers_mixed_lang:",
                results,
                end_time - start_time)
        )
