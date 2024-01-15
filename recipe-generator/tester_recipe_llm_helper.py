import os
import time
import unittest
from openai import AzureOpenAI
from recipe_llm_helper import RecipeLlmHelper



class TestRecipeLlmHelper(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestRecipeLlmHelper, self).__init__(*args, **kwargs)
        # Custom fields
        self.azure_openai_model_name = os.getenv('AZURE_OPENAI_GPT_DEPLOYMENT')
        self.azure_openai_client = AzureOpenAI(api_version="2023-09-01-preview")
        self.recipe_llm_helper = RecipeLlmHelper(self.azure_openai_client, self.azure_openai_model_name)
        self.test_generate_recipe_data_mix = []

        with open('./test_data/test_generate_recipe_mix.txt', 'r') as file:
            for line in file:
                sentence = line.split(" - ")
                self.test_generate_recipe_data_mix.append([sentence[0], sentence[1]])

    def test_generate_recipe(self):
        start_time = time.time()
        for input in self.test_generate_recipe_data_mix:
            self.recipe_llm_helper.generate_recipe(input[0], input[1])
        end_time = time.time()
        print(f"(Mix Batch Data) Elaspsed Time (seconds): {end_time - start_time}")

    def test_generate_recipe_full_response(self):
        start_time = time.time()
        token_count = 0.0
        for input in self.test_generate_recipe_data_mix:
            response = self.recipe_llm_helper.generate_recipe(input[0], input[1])
            token_count += response.usage.total_tokens
        end_time = time.time()
        print(f"(Mix Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / 100.0}")



if __name__ == "__main__":
    unittest.main()
