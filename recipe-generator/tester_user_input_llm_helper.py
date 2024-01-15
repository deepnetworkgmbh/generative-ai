import os
import time
import unittest
from openai import AzureOpenAI
from user_input_llm_helper import UserInputLlmHelper



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

    def test_dish_time_count_english_batch(self):
        start_time = time.time()
        token_count = 0
        for input_sentence in self.test_dish_data_english:
            response = self.user_input_llm_helper.clean_dish_name(input_sentence, 'English')
            token_count += response.usage.total_tokens
        end_time = time.time()
        print(f"(English Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / 50.0}")

    def test_dish_time_count_german_batch(self):
        start_time = time.time()
        token_count = 0
        for input_sentence in self.test_dish_data_german:
            response = self.user_input_llm_helper.clean_dish_name(input_sentence, 'German')
            token_count += response.usage.total_tokens
        end_time = time.time()
        print(f"(German Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / 50.0}")

    def test_dish_time_count_turkish_batch(self):
        start_time = time.time()
        token_count = 0
        for input_sentence in self.test_dish_data_turkish:
            response = self.user_input_llm_helper.clean_dish_name(input_sentence, 'Turkish')
            token_count += response.usage.total_tokens
        end_time = time.time()
        print(f"(Turkish Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / 50.0}")

    def test_count_time_count_english_batch(self):
        start_time = time.time()
        token_count = 0
        for input_sentence in self.test_count_data_english:
            response = self.user_input_llm_helper.clean_servings_size(input_sentence, 'English')
            token_count += response.usage.total_tokens
        end_time = time.time()
        print(f"(English Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / 50.0}")

    def test_count_time_count_german_batch(self):
        start_time = time.time()
        token_count = 0
        for input_sentence in self.test_dish_data_german:
            response = self.user_input_llm_helper.clean_servings_size(input_sentence, 'German')
            token_count += response.usage.total_tokens
        end_time = time.time()
        print(f"(German Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / 50.0}")

    def test_count_time_count_turkish_batch(self):
        start_time = time.time()
        token_count = 0
        for input_sentence in self.test_count_data_turkish:
            response = self.user_input_llm_helper.clean_dish_name(input_sentence, 'Turkish')
            token_count += response.usage.total_tokens
        end_time = time.time()
        print(f"(Turkish Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / 50.0}")

    def test_language(self):
        start_time = time.time()
        success_count = 0.0
        for input_sentence_language in self.test_language_data_mix:
            response = self.user_input_llm_helper.ask_language(input_sentence_language[0])
            if response.strip().lower() == input_sentence_language[1].strip().lower():
                success_count += 1.0
        end_time = time.time()
        print(f"(Mix Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Success rate: {success_count}")

    def test_type_match(self):
        start_time = time.time()
        success_count = 0.0
        for input in self.test_type_match_data:
            response = self.user_input_llm_helper.does_input_type_match(input[0], input[2], input[1])
            if response:
                success_count += 1.0
        end_time = time.time()
        print(f"(Mix Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Success rate: {success_count * 2.0}")

if __name__ == "__main__":
    unittest.main()
