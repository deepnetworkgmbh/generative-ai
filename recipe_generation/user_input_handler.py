import json
import logging
import os
from enum import Enum
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk
from openai.lib.azure import AzureOpenAI

import logging_helper
from azure_speech_helper import create_speech_recognizer
from user_input_llm_helper import UserInputLlmHelper


class UserInputType(Enum):
    DISH_NAME = 1
    SERVINGS = 2


def _eliminate_punctuations(user_input):
    eliminated_sentence = user_input
    characters_to_replace = [',', '.', ':', ';', '"', '\'', "?", "!"]

    # Replace specified characters with a space
    for char in characters_to_replace:
        eliminated_sentence = eliminated_sentence.replace(char, ' ')

    return eliminated_sentence


class UserInputHandler:
    def __init__(self, user_input_llm_helper: UserInputLlmHelper, speech_recognizer: speechsdk.SpeechRecognizer):
        self.llm_helper = user_input_llm_helper
        self.speech_recognizer = speech_recognizer

    def _clean_dish_input(self, user_input: str, language: str):
        cleaned_dish_name = self.llm_helper.clean_dish_name(user_input, language)
        cleaned_dish_name_json = json.loads(cleaned_dish_name.choices[0].message.content)
        if not cleaned_dish_name_json['is_valid']:
            logging.debug("(First Check) Input does not contain a valid dish name. ")
            return None

        logging.debug("(First Check) Cleaned dish name: " + str(cleaned_dish_name_json['dish_name']))

        if not self.llm_helper.does_input_type_match(cleaned_dish_name_json['dish_name'], "dish name", language):
            logging.debug("(Second Check): Input is not a real dish name.")
            return None

        return cleaned_dish_name_json['dish_name']

    def _clean_servings_input(self, user_input: str, language: str):
        cleaned_servings = self.llm_helper.clean_servings(user_input, language)
        cleaned_servings_json = json.loads(cleaned_servings.choices[0].message.content)

        if not cleaned_servings_json['is_valid']:
            logging.debug("(First Check) Input does not contain a valid servings size. ")
            return None

        logging.debug("(First Check) Cleaned servings size " + str(cleaned_servings_json['number_of_people']))

        if not self.llm_helper.does_input_type_match(cleaned_servings_json['number_of_people'], "integer",
                                                     language):
            logging.debug("(Second Check): Input is not a real servings size.")
            return None

        return cleaned_servings_json['number_of_people']

    # Return None if input is not valid, or the cleaned text/number.
    def clean_input(self, user_input: str, input_type: UserInputType, input_language):
        user_input = _eliminate_punctuations(user_input)
        # Getting language of user prompt
        language = input_language
        if input_language is None:
            language = self.llm_helper.determine_language(user_input).choices[0].message.content
        logging.debug("Language is: " + language)

        if input_type == UserInputType.DISH_NAME:
            return self._clean_dish_input(user_input, language)
        elif input_type == UserInputType.SERVINGS:
            return self._clean_servings_input(user_input, language)
        else:
            logging.debug("Error case")
            return None

    def get_dish_name_and_servings_using_speech(self):
        scraped_values = {
            'dish_name': self.get_speech_input_from_user(self.speech_recognizer, "Tell the dish name: ",
                                                         UserInputType.DISH_NAME),
            'servings': self.get_speech_input_from_user(self.speech_recognizer,
                                                        "Tell how many servings (Number of people): ",
                                                        UserInputType.SERVINGS)
        }
        return scraped_values

    def get_speech_input_from_user(self, speech_recognizer, message, user_input_type: UserInputType):
        while True:
            print(message)
            user_input = speech_recognizer.recognize_once()
            logging.debug("User entered: ", user_input.text)
            detected_language = speechsdk.AutoDetectSourceLanguageResult(user_input).language

            if user_input.reason == speechsdk.ResultReason.RecognizedSpeech:
                cleaned_input = self.clean_input(user_input.text, user_input_type, None)
                if cleaned_input:
                    return cleaned_input
                else:
                    print(f"Please specify a valid {user_input_type.name}.")
                    continue
            elif user_input.reason == speechsdk.ResultReason.Canceled:
                logging.info("Speech input cancelled. Exiting.")
                cancellation_details = user_input.cancellation_details
                logging.debug("Speech Recognition canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    logging.warning("Error details: {}".format(cancellation_details.error_details))
                    logging.warning("Did you set the speech resource key and region values?")
                return None
            else:
                print("Speech is not recognized. Please try again.")
                continue

    def get_text_input_from_user(self, message, user_input_type: UserInputType):
        while True:
            user_input = input(message)
            cleaned_input = self.clean_input(user_input, user_input_type, None)
            logging.debug("Cleaned Input: %s", cleaned_input)
            if cleaned_input:
                return cleaned_input
            else:
                print(f"Please enter a valid {user_input_type.name}")
                continue

    def get_dish_name_and_servings_using_text(self):
        # while True:
        scraped_values = {
            'dish_name': self.get_text_input_from_user("Tell the dish name: ", UserInputType.DISH_NAME),
            'servings': self.get_text_input_from_user("Tell how many servings (Number of people): ",
                                                      UserInputType.SERVINGS)
        }
        return scraped_values

    def get_dish_name_and_servings(self):
        output_data = None

        while output_data is None:
            user_input = input("Select input type: \n 1) Text \n 2) Speech \n q) Quit \n")
            if user_input == "1":
                output_data = self.get_dish_name_and_servings_using_text()
            elif user_input == "2":
                output_data = self.get_dish_name_and_servings_using_speech()
            elif user_input == "q":
                exit(0)
            else:
                logging.debug("Error Input")

        return output_data['dish_name'], output_data['servings']


if __name__ == "__main__":
    logging_helper.setup_logging(f'{Path(__file__).stem}.log')

    azure_openai_model_name = os.getenv('AZURE_OPENAI_GPT_DEPLOYMENT')
    azure_openai = AzureOpenAI(api_version="2023-09-01-preview")

    speech_recognizer = create_speech_recognizer()
    user_input_llm_helper = UserInputLlmHelper(azure_openai, azure_openai_model_name)

    user_input_handler = UserInputHandler(user_input_llm_helper, speech_recognizer)
    dish_name, servings = user_input_handler.get_dish_name_and_servings()
    if dish_name:
        print(f"DISH: {dish_name}")
        print(f"SERVINGS: {servings}")
