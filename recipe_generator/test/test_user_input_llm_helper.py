import json
import os
import time
import unittest
from openai import AzureOpenAI
from recipe_generator.user_input_llm_helper import UserInputLlmHelper
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

        with open('test_data/dish_name_in_sentences_english.txt', 'r') as file:
            for line in file:
                self.dish_name_in_sentences_english.append(line.strip())

        with open('test_data/dish_name_in_sentences_german.txt', 'r') as file:
            for line in file:
                self.dish_name_in_sentences_german.append(line.strip())

        with open('test_data/dish_name_in_sentences_turkish.txt', 'r') as file:
            for line in file:
                self.dish_name_in_sentences_turkish.append(line.strip())

        with open('test_data/number_in_sentences_english.txt', 'r') as file:
            for line in file:
                self.number_in_sentences_english.append(line.strip())

        with open('test_data/number_in_sentences_german.txt', 'r') as file:
            for line in file:
                self.number_in_sentences_german.append(line.strip())

        with open('test_data/number_in_sentences_turkish.txt', 'r') as file:
            for line in file:
                self.number_in_sentences_turkish.append(line.strip())

        with open('test_data/dish_name_and_number_in_sentences_mixed_lang.txt', 'r') as file:
            for line in file:
                sentence = line.split(" - ")
                self.dish_name_and_number_in_sentences_mixed_lang.append([sentence[0], sentence[1]])

        with open('test_data/dish_name_or_number_in_sentences_mixed_lang.txt', 'r') as file:
            for line in file:
                sentence = line.split(" - ")
                self.dish_name_or_number_in_sentences_mixed_lang.append([sentence[0], sentence[1], sentence[2]])

    def test_clean_dish_name_english(self):
        results, total_time = run_clean_dish_name(self.user_input_llm_helper, self.dish_name_in_sentences_english, "English")
        test_helpers.calculate_and_print_metrics(
            "Clean Dish Name: dish_name_in_sentences_english:",
            results,
            total_time
        )

    def test_clean_dish_name_german(self):
        results, total_time = run_clean_dish_name(self.user_input_llm_helper, self.dish_name_in_sentences_german, "German")
        test_helpers.calculate_and_print_metrics(
            "Clean Dish Name: dish_name_in_sentences_german:",
            results,
            total_time
        )

    def test_clean_dish_name_turkish(self):
        results, total_time = run_clean_dish_name(self.user_input_llm_helper, self.dish_name_in_sentences_turkish, "Turkish")
        end_time = time.time()
        test_helpers.calculate_and_print_metrics(
            "Clean Dish Name: dish_name_in_sentences_turkish:",
            results,
            total_time
        )

    def test_clean_servings_english(self):
        results, total_time = run_clean_servings(self.user_input_llm_helper, self.number_in_sentences_english, "English")
        test_helpers.calculate_and_print_metrics(
            "Clean Servings: number_in_sentences_english:",
            results,
            total_time
        )

    def test_clean_servings_german(self):
        results, total_time = run_clean_servings(self.user_input_llm_helper, self.dish_name_in_sentences_german, "German")
        test_helpers.calculate_and_print_metrics(
            "Clean Servings: dish_name_in_sentences_german:",
            results,
            total_time
        )

    def test_clean_servings_turkish(self):
        results, total_time = run_clean_servings(self.user_input_llm_helper, self.number_in_sentences_turkish, "Turkish")
        test_helpers.calculate_and_print_metrics(
            "Clean Servings: number_in_sentences_turkish:",
            results,
            total_time
        )

    def test_determine_language_mixed_lang(self):
        results, total_time = run_determine_language(self.user_input_llm_helper, self.dish_name_and_number_in_sentences_mixed_lang)
        test_helpers.calculate_and_print_metrics(
            "Determine Language: dish_name_and_number_in_sentences_mixed_lang:",
            results,
            total_time
        )

    def test_does_input_type_match(self):
        results, total_time = run_check_input_type_match(self.user_input_llm_helper, self.dish_name_or_number_in_sentences_mixed_lang)
        test_helpers.calculate_and_print_metrics(
            "Does Input Type Match: dish_name_or_number_in_sentences_mixed_lang:",
            results,
            total_time
        )


def run_clean_dish_name(user_input_llm_helper, data, language):
    start_time = time.time()
    results = []
    for input_sentence in data:
        response = user_input_llm_helper.clean_dish_name(input_sentence, language)
        results.append({
            "completion_tokens": response.usage.completion_tokens,
            "prompt_tokens": response.usage.prompt_tokens
        })
    end_time = time.time()
    return results, (end_time - start_time)


def run_clean_servings(user_input_llm_helper, data, language):
    start_time = time.time()
    results = []
    for input_sentence in data:
        response = user_input_llm_helper.clean_servings(input_sentence, language)
        results.append({
            "completion_tokens": response.usage.completion_tokens,
            "prompt_tokens": response.usage.prompt_tokens
        })
    end_time = time.time()
    return results, (end_time - start_time)


def run_determine_language(user_input_llm_helper, data):
    start_time = time.time()
    results = []
    for input in data:
        response = user_input_llm_helper.determine_language(input[0])
        results.append({
            "completion_tokens": response.usage.completion_tokens,
            "prompt_tokens": response.usage.prompt_tokens
        })
    end_time = time.time()
    return results, (end_time - start_time)


def run_check_input_type_match(user_input_llm_helper, data):
    start_time = time.time()
    results = []
    for input in data:
        response = user_input_llm_helper.check_input_type_match(input[0], input[2], input[1])
        results.append({
            "completion_tokens": response.usage.completion_tokens,
            "prompt_tokens": response.usage.prompt_tokens
        })
    end_time = time.time()
    return results, (end_time - start_time)
