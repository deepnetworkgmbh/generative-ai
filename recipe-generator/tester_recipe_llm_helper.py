import os
import time
import unittest
from openai import AzureOpenAI
from recipe_llm_helper import RecipeLlmHelper, format_prompt
import tester_constants

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
        token_count = 0.0
        for input in self.test_generate_recipe_data_mix:
            prompt = format_prompt(input[0], input[1])
            response = self.recipe_llm_helper.generate_completion(prompt)
            token_count += response.usage.total_tokens
        end_time = time.time()
        print("GENERATE RECIPE Test - Mixed")
        print(f"(Mix Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {((token_count) / float(tester_constants.GENERATE_RECIPE) * 100.0)}")
        print(f"Cost: {response.usage.completion_tokens * 0.000001 + response.usage.prompt_tokens * 0.000002}")

if __name__ == "__main__":
    unittest.main()
