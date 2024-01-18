import json
import os
import time
import unittest
from openai import AzureOpenAI
from ..user_input_llm_helper import UserInputLlmHelper
import test_helpers


class TestUserInputLlmHelper(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestUserInputLlmHelper, self).__init__(*args, **kwargs)
        # Custom fields
        self.azure_openai_model_name = os.getenv('AZURE_OPENAI_GPT_DEPLOYMENT')
        self.azure_openai_client = AzureOpenAI(api_version="2023-09-01-preview")
        self.user_input_llm_helper = UserInputLlmHelper(self.azure_openai_client, self.azure_openai_model_name)
        self.dish_name_in_sentences_english = []
        self.dish_name_in_sentences_german = []
        self.dish_name_in_sentences_turkish = []
        self.number_in_sentences_english = []
        self.number_in_sentences_german = []
        self.number_in_sentences_turkish = []
        self.dish_name_and_number_in_sentences_mixed_lang = []
        self.dish_name_or_number_in_sentences_mixed_lang = []

        with open('./test_data/dish_name_in_sentences_english.txt', 'r') as file:
            for line in file:
                self.dish_name_in_sentences_english.append(line.strip())

        with open('./test_data/dish_name_in_sentences_german.txt', 'r') as file:
            for line in file:
                self.dish_name_in_sentences_german.append(line.strip())

        with open('./test_data/dish_name_in_sentences_turkish.txt', 'r') as file:
            for line in file:
                self.dish_name_in_sentences_turkish.append(line.strip())

        with open('./test_data/number_in_sentences_english.txt', 'r') as file:
            for line in file:
                self.number_in_sentences_english.append(line.strip())

        with open('./test_data/number_in_sentences_german.txt', 'r') as file:
            for line in file:
                self.number_in_sentences_german.append(line.strip())

        with open('./test_data/number_in_sentences_turkish.txt', 'r') as file:
            for line in file:
                self.number_in_sentences_turkish.append(line.strip())

        with open('./test_data/dish_name_and_number_in_sentences_mixed_lang.txt', 'r') as file:
            for line in file:
                sentence = line.split(" - ")
                self.dish_name_and_number_in_sentences_mixed_lang.append([sentence[0], sentence[1]])

        with open('./test_data/dish_name_or_number_in_sentences_mixed_lang.txt', 'r') as file:
            for line in file:
                sentence = line.split(" - ")
                self.dish_name_or_number_in_sentences_mixed_lang.append([sentence[0], sentence[1], sentence[2]])

    def test_clean_dish_name_english(self):
        start_time = time.time()
        results = []

        for input_sentence in self.dish_name_in_sentences_english:
            response = self.user_input_llm_helper.clean_dish_name(input_sentence, 'English')
            results.append({
                "completion_tokens": response.usage.completion_tokens,
                "prompt_tokens": response.usage.prompt_tokens
            })

        end_time = time.time()
        test_helpers.calculate_and_print_metrics(
            "Clean Dish Name: dish_name_in_sentences_english:",
            results,
            end_time - start_time
        )

    def test_clean_dish_name_german(self):
        start_time = time.time()
        results = []

        for input_sentence in self.dish_name_in_sentences_german:
            response = self.user_input_llm_helper.clean_dish_name(input_sentence, 'German')
            results.append({
                "completion_tokens": response.usage.completion_tokens,
                "prompt_tokens": response.usage.prompt_tokens
            })

        end_time = time.time()
        test_helpers.calculate_and_print_metrics(
            "Clean Dish Name: dish_name_in_sentences_german:",
            results,
            end_time - start_time
        )


def test_clean_dish_name_turkish(self):
        start_time = time.time()
        results = []

        for input_sentence in self.dish_name_in_sentences_turkish:
            response = self.user_input_llm_helper.clean_dish_name(input_sentence, 'Turkish')
            results.append({
                "completion_tokens": response.usage.completion_tokens,
                "prompt_tokens": response.usage.prompt_tokens
            })

        end_time = time.time()
        test_helpers.calculate_and_print_metrics(
            "Clean Dish Name: dish_name_in_sentences_turkish:",
            results,
            end_time - start_time
        )


def test_clean_servings_english(self):
        start_time = time.time()
        results = []

        for input_sentence in self.number_in_sentences_english:
            response = self.user_input_llm_helper.clean_servings_size(input_sentence, 'English')
            results.append({
                "completion_tokens": response.usage.completion_tokens,
                "prompt_tokens": response.usage.prompt_tokens
            })

        end_time = time.time()
        print("SERVING SIZE Test - English")
        print(f"(English Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / float(test_helpers.COUNT_DATA_ENGLISH)}")
        print(f"Cost: {response.usage.prompt_tokens * 0.000001 + response.usage.completion_tokens * 0.000002}")
        test_helpers.calculate_and_print_metrics(
            "Clean Dish Name: dish_name_in_sentences_english:",
            results,
            end_time - start_time
        )


def test_clean_servings_german(self):
        start_time = time.time()
        results = []

        for input_sentence in self.dish_name_in_sentences_german:
            response = self.user_input_llm_helper.clean_servings_size(input_sentence, 'German')
            results.append({
                "completion_tokens": response.usage.completion_tokens,
                "prompt_tokens": response.usage.prompt_tokens
            })
        end_time = time.time()
        print("SERVING SIZE Test - German")
        print(f"(German Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / float(test_helpers.COUNT_DATA_GERMAN)}")
        print(f"Cost: {response.usage.prompt_tokens * 0.000001 + response.usage.completion_tokens * 0.000002}")
        test_helpers.calculate_and_print_metrics(
            "Clean Dish Name: dish_name_in_sentences_english:",
            results,
            end_time - start_time
        )


def test_clean_servings_turkish(self):
        start_time = time.time()
        results = []

        for input_sentence in self.number_in_sentences_turkish:
            response = self.user_input_llm_helper.clean_dish_name(input_sentence, 'Turkish')
            results.append({
                "completion_tokens": response.usage.completion_tokens,
                "prompt_tokens": response.usage.prompt_tokens
            })
        end_time = time.time()
        print("SERVING SIZE Test - Turkish")
        print(f"(Turkish Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / float(test_helpers.COUNT_DATA_TURKISH)}")
        print(f"Cost: {response.usage.prompt_tokens * 0.000001 + response.usage.completion_tokens * 0.000002}")
        test_helpers.calculate_and_print_metrics(
            "Clean Dish Name: dish_name_in_sentences_english:",
            results,
            end_time - start_time
        )


def test_determine_language_mixed_lang(self):
        start_time = time.time()
        results = []

        success_count = 0.0
        for input in self.dish_name_and_number_in_sentences_mixed_lang:
            response = self.user_input_llm_helper.ask_language_full_response(input[0])
            results.append({
                "completion_tokens": response.usage.completion_tokens,
                "prompt_tokens": response.usage.prompt_tokens
            })
            if response.choices[0].message.content.strip().lower() == input[1].strip().lower():
                success_count += 1.0
        end_time = time.time()
        print("LANGUAGE Test - Mix")
        print(f"(Mix Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / float(test_helpers.LANGUAGE_DATA)}")
        print(f"Success rate: {((success_count / float(test_helpers.LANGUAGE_DATA))) * 100.0}")
        print(f"Cost: {response.usage.prompt_tokens * 0.000001 + response.usage.completion_tokens * 0.000002}")
        test_helpers.calculate_and_print_metrics(
            "Clean Dish Name: dish_name_in_sentences_english:",
            results,
            end_time - start_time
        )


def test_type_match(self):
        start_time = time.time()
        results = []

        for input in self.sentences_language_type_mix:
            response = self.user_input_llm_helper.does_input_type_match_full_response(input[0], input[2], input[1])
            results.append({
                "completion_tokens": response.usage.completion_tokens,
                "prompt_tokens": response.usage.prompt_tokens
            })
            if json.loads(response.choices[0].message.content)['is_correct_type']:
                success_count += 1.0
        end_time = time.time()
        print("TYPE MATCH Test - Mix")
        print(f"(Mix Batch Data) Elaspsed Time (seconds): {end_time - start_time}")
        print(f"Total token: {token_count}")
        print(f"Average token: {float(token_count) / float(test_helpers.TYPE_MATCH)}")
        print(f"Success rate: {((success_count / float(test_helpers.TYPE_MATCH)) * 100.0)}")
        print(f"Cost: {response.usage.prompt_tokens * 0.000001 + response.usage.completion_tokens * 0.000002}")
        test_helpers.calculate_and_print_metrics(
            "Clean Dish Name: dish_name_in_sentences_english:",
            results,
            end_time - start_time
        )


if __name__ == "__main__":
    unittest.main()
