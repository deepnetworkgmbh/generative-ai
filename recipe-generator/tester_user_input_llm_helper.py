import json
import os
import time
import unittest
from openai import AzureOpenAI
from user_input_llm_helper import UserInputLlmHelper
import tester_constants



class TestUserInputLlmHelper(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestUserInputLlmHelper, self).__init__(*args, **kwargs)
        # Custom fields
        self.azure_openai_model_name = os.getenv('AZURE_OPENAI_GPT_DEPLOYMENT')
        self.azure_openai_client = AzureOpenAI(api_version="2023-09-01-preview")
        self.user_input_llm_helper = UserInputLlmHelper(self.azure_openai_client, self.azure_openai_model_name)
        self.test_dish_data_english = []
        self.test_dish_data_german = []
        self.test_dish_data_turkish = []
        self.test_count_data_english = []
        self.test_count_data_german = []
        self.test_count_data_turkish = []
        self.test_language_data_mix = []
        self.test_type_match_data = []

        with open('./test_data/test_dish_data_english.txt', 'r') as file:
            for line in file:
                self.test_dish_data_english.append(line.strip())

        with open('./test_data/test_dish_data_german.txt', 'r') as file:
            for line in file:
                self.test_dish_data_german.append(line.strip())

        with open('./test_data/test_dish_data_turkish.txt', 'r') as file:
            for line in file:
                self.test_dish_data_turkish.append(line.strip())

        with open('./test_data/test_count_data_english.txt', 'r') as file:
            for line in file:
                self.test_count_data_english.append(line.strip())

        with open('./test_data/test_count_data_german.txt', 'r') as file:
            for line in file:
                self.test_count_data_german.append(line.strip())

        with open('./test_data/test_count_data_turkish.txt', 'r') as file:
            for line in file:
                self.test_count_data_turkish.append(line.strip())

        with open('./test_data/test_language_data_mix.txt', 'r') as file:
            for line in file:
                sentence = line.split(" - ")
                self.test_language_data_mix.append([sentence[0], sentence[1]])

        with open('./test_data/test_type_match_data.txt', 'r') as file:
            for line in file:
                sentence = line.split(" - ")
                self.test_type_match_data.append([sentence[0], sentence[1], sentence[2]])

    def test_dish_time_token_english_batch(self):
        start_time = time.time()
        token_count = 0
        for input_sentence in self.test_dish_data_english:
            response = self.user_input_llm_helper.clean_dish_name(input_sentence, 'English')
            token_count += response.usage.total_tokens
        end_time = time.time()
        print("DISH Test - English")
        print(f"(English Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / float(tester_constants.DISH_DATA_ENGLISH)}")
        print(f"Cost: {response.usage.completion_tokens * 0.000001 + response.usage.prompt_tokens * 0.000002}")

    def test_dish_time_token_german_batch(self):
        start_time = time.time()
        token_count = 0
        for input_sentence in self.test_dish_data_german:
            response = self.user_input_llm_helper.clean_dish_name(input_sentence, 'German')
            token_count += response.usage.total_tokens
        end_time = time.time()
        print("DISH Test - German")
        print(f"(German Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / float(tester_constants.DISH_DATA_GERMAN)}")
        print(f"Cost: {response.usage.completion_tokens * 0.000001 + response.usage.prompt_tokens * 0.000002}")

    def test_dish_time_token_turkish_batch(self):
        start_time = time.time()
        token_count = 0
        for input_sentence in self.test_dish_data_turkish:
            response = self.user_input_llm_helper.clean_dish_name(input_sentence, 'Turkish')
            token_count += response.usage.total_tokens
        end_time = time.time()
        print("DISH Test - Turkish")
        print(f"(Turkish Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / float(tester_constants.DISH_DATA_TURKISH)}")
        print(f"Cost: {response.usage.completion_tokens * 0.000001 + response.usage.prompt_tokens * 0.000002}")

    def test_count_time_token_english_batch(self):
        start_time = time.time()
        token_count = 0
        for input_sentence in self.test_count_data_english:
            response = self.user_input_llm_helper.clean_servings_size(input_sentence, 'English')
            token_count += response.usage.total_tokens
        end_time = time.time()
        print("SERVING SIZE Test - English")
        print(f"(English Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / float(tester_constants.COUNT_DATA_ENGLISH)}")
        print(f"Cost: {response.usage.completion_tokens * 0.000001 + response.usage.prompt_tokens * 0.000002}")

    def test_count_time_token_german_batch(self):
        start_time = time.time()
        token_count = 0
        for input_sentence in self.test_dish_data_german:
            response = self.user_input_llm_helper.clean_servings_size(input_sentence, 'German')
            token_count += response.usage.total_tokens
        end_time = time.time()
        print("SERVING SIZE Test - German")
        print(f"(German Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / float(tester_constants.COUNT_DATA_GERMAN)}")
        print(f"Cost: {response.usage.completion_tokens * 0.000001 + response.usage.prompt_tokens * 0.000002}")

    def test_count_time_token_turkish_batch(self):
        start_time = time.time()
        token_count = 0
        for input_sentence in self.test_count_data_turkish:
            response = self.user_input_llm_helper.clean_dish_name(input_sentence, 'Turkish')
            token_count += response.usage.total_tokens
        end_time = time.time()
        print("SERVING SIZE Test - Turkish")
        print(f"(Turkish Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / float(tester_constants.COUNT_DATA_TURKISH)}")
        print(f"Cost: {response.usage.completion_tokens * 0.000001 + response.usage.prompt_tokens * 0.000002}")

    def test_language(self):
        start_time = time.time()
        token_count = 0
        success_count = 0.0
        for input in self.test_language_data_mix:
            response = self.user_input_llm_helper.ask_language_full_response(input[0])
            token_count += response.usage.total_tokens
            if response.choices[0].message.content.strip().lower() == input[1].strip().lower():
                success_count += 1.0
        end_time = time.time()
        print("LANGUAGE Test - Mix")
        print(f"(Mix Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / float(tester_constants.LANGUAGE_DATA)}")
        print(f"Success rate: {((success_count / float(tester_constants.LANGUAGE_DATA))) * 100.0}")
        print(f"Cost: {response.usage.completion_tokens * 0.000001 + response.usage.prompt_tokens * 0.000002}")

    def test_type_match(self):
        start_time = time.time()
        token_count = 0
        success_count = 0.0
        for input in self.test_type_match_data:
            response = self.user_input_llm_helper.does_input_type_match_full_response(input[0], input[2], input[1])
            token_count += response.usage.total_tokens
            if json.loads(response.choices[0].message.content)['is_correct_type']:
                success_count += 1.0
        end_time = time.time()
        print("TYPE MATCH Test - Mix")
        print(f"(Mix Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / float(tester_constants.TYPE_MATCH)}")
        print(f"Success rate: {((success_count / float(tester_constants.TYPE_MATCH)) * 100.0)}")
        print(f"Cost: {response.usage.completion_tokens * 0.000001 + response.usage.prompt_tokens * 0.000002}")

if __name__ == "__main__":
    unittest.main()
