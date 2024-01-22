import json
import os
import time
import unittest
from pathlib import Path

from openai import AzureOpenAI

import test_helpers
from recipe_generation.user_input_llm_helper import UserInputLlmHelper


class TestUserInputLlmHelper(unittest.TestCase):
    dish_name_in_sentences_english = []
    dish_name_in_sentences_german = []
    dish_name_in_sentences_turkish = []
    number_in_sentences_english = []
    number_in_sentences_german = []
    number_in_sentences_turkish = []
    dish_name_or_number_mixed_lang = []
    dish_name_or_number_in_sentences_mixed_lang = []
    test_metrics = []

    @classmethod
    def setUpClass(cls):
        azure_openai_model_name = os.getenv('AZURE_OPENAI_GPT_DEPLOYMENT')
        azure_openai_client = AzureOpenAI(api_version="2023-09-01-preview")
        cls.user_input_llm_helper = UserInputLlmHelper(azure_openai_client, azure_openai_model_name)

        with open('test_data/dish_name_in_sentences_english.txt', 'r') as file:
            for line in file:
                cls.dish_name_in_sentences_english.append(line.strip())

        with open('test_data/dish_name_in_sentences_german.txt', 'r') as file:
            for line in file:
                cls.dish_name_in_sentences_german.append(line.strip())

        with open('test_data/dish_name_in_sentences_turkish.txt', 'r') as file:
            for line in file:
                cls.dish_name_in_sentences_turkish.append(line.strip())

        with open('test_data/number_in_sentences_english.txt', 'r') as file:
            for line in file:
                cls.number_in_sentences_english.append(line.strip())

        with open('test_data/number_in_sentences_german.txt', 'r') as file:
            for line in file:
                cls.number_in_sentences_german.append(line.strip())

        with open('test_data/number_in_sentences_turkish.txt', 'r') as file:
            for line in file:
                cls.number_in_sentences_turkish.append(line.strip())

        with open('test_data/dish_name_or_number_in_sentences_mixed_lang.txt', 'r') as file:
            for line in file:
                sentence = line.split(" - ")
                cls.dish_name_or_number_in_sentences_mixed_lang.append([sentence[0], sentence[1]])

        with open('test_data/dish_name_or_number_mixed_lang.txt', 'r') as file:
            for line in file:
                sentence = line.split(" - ")
                cls.dish_name_or_number_mixed_lang.append([sentence[0], sentence[1], sentence[2]])

    @classmethod
    def tearDownClass(cls):
        with open(f'{Path(__file__).stem}_results.json', 'w') as file:
            json.dump(cls.test_metrics, file, indent=2)

    def test_clean_dish_name_english(self):
        results, total_time = self.run_clean_dish_name(self.dish_name_in_sentences_english,
                                                  "English")
        self.test_metrics.append(
            test_helpers.calculate_metrics(
                "Clean Dish Name: dish_name_in_sentences_english:",
                results,
                total_time
            )
        )

    def test_clean_dish_name_german(self):
        results, total_time = self.run_clean_dish_name(self.dish_name_in_sentences_german,
                                                  "German")
        self.test_metrics.append(
            test_helpers.calculate_metrics(
                "Clean Dish Name: dish_name_in_sentences_german:",
                results,
                total_time
            )
        )

    def test_clean_dish_name_turkish(self):
        results, total_time = self.run_clean_dish_name(self.dish_name_in_sentences_turkish,
                                                  "Turkish")
        self.test_metrics.append(
            test_helpers.calculate_metrics(
                "Clean Dish Name: dish_name_in_sentences_turkish:",
                results,
                total_time
            )
        )

    def test_clean_servings_english(self):
        results, total_time = self.run_clean_servings(self.number_in_sentences_english,"English")
        self.test_metrics.append(
            test_helpers.calculate_metrics(
                "Clean Servings: number_in_sentences_english:",
                results,
                total_time
            )
        )

    def test_clean_servings_german(self):
        results, total_time = self.run_clean_servings(self.number_in_sentences_german,"German")
        self.test_metrics.append(
            test_helpers.calculate_metrics(
                "Clean Servings: dish_name_in_sentences_german:",
                results,
                total_time
            )
        )

    def test_clean_servings_turkish(self):
        results, total_time = self.run_clean_servings(self.number_in_sentences_turkish,"Turkish")
        self.test_metrics.append(
            test_helpers.calculate_metrics(
                "Clean Servings: number_in_sentences_turkish:",
                results,
                total_time
            )
        )

    def test_determine_language_mixed_lang(self):
        results, total_time = self.run_determine_language(self.dish_name_or_number_in_sentences_mixed_lang)
        self.test_metrics.append(
            test_helpers.calculate_metrics(
                "Determine Language: dish_name_or_number_in_sentences_mixed_lang:",
                results,
                total_time
            )
        )

    def test_does_input_type_match(self):
        results, total_time = self.run_check_input_type_match(self.dish_name_or_number_mixed_lang)
        self.test_metrics.append(
            test_helpers.calculate_metrics(
                "Does Input Type Match: dish_name_or_number_mixed_lang:",
                results,
                total_time
            )
        )

    def run_clean_dish_name(self, data, language):
        start_time = time.time()
        results = []
        for input_sentence in data:
            response = self.user_input_llm_helper.clean_dish_name(input_sentence, language)
            results.append({
                "completion_tokens": response.usage.completion_tokens,
                "prompt_tokens": response.usage.prompt_tokens
            })
            try:
                cleaned_servings_json = json.loads(response.choices[0].message.content)
                self.assertEqual(True, cleaned_servings_json['is_valid'], f"Got is_valid False for: {input_sentence}")
            except json.decoder.JSONDecodeError:
                self.fail("Non-valid JSON")
        end_time = time.time()
        return results, (end_time - start_time)

    def run_clean_servings(self, data, language):
        start_time = time.time()
        results = []
        for input_sentence in data:
            response = self.user_input_llm_helper.clean_servings(input_sentence, language)
            results.append({
                "completion_tokens": response.usage.completion_tokens,
                "prompt_tokens": response.usage.prompt_tokens
            })
            try:
                cleaned_servings_json = json.loads(response.choices[0].message.content)
                self.assertEqual(True, cleaned_servings_json['is_valid'], f"Got is_valid False for: {input_sentence}")
            except json.decoder.JSONDecodeError:
                self.fail("Non-valid JSON")
        end_time = time.time()
        return results, (end_time - start_time)

    def run_determine_language(self, data):
        start_time = time.time()
        results = []
        for input in data:
            response = self.user_input_llm_helper.determine_language(input[0])
            results.append({
                "completion_tokens": response.usage.completion_tokens,
                "prompt_tokens": response.usage.prompt_tokens
            })
            try:
                response_language = response.choices[0].message.content
                self.assertEqual(input[1].strip(), response_language, f"Got wrong language for: {input}")
            except:
                print(f"Non-valid String: {input}")
        end_time = time.time()
        return results, (end_time - start_time)

    def run_check_input_type_match(self, data):
        start_time = time.time()
        results = []
        for input in data:
            response = self.user_input_llm_helper.check_input_type_match(input[0], input[2], input[1].split())
            results.append({
                "completion_tokens": response.usage.completion_tokens,
                "prompt_tokens": response.usage.prompt_tokens
            })
            try:
                cleaned_servings_json = json.loads(response.choices[0].message.content)
                self.assertEqual(True, cleaned_servings_json['is_correct_type'], f"Got is_valid False for: {input}")
            except json.decoder.JSONDecodeError:
                self.fail("Non-valid JSON")
        end_time = time.time()
        return results, (end_time - start_time)
