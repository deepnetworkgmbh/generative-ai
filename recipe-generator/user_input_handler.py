import json
import os
from enum import Enum
import azure.cognitiveservices.speech as speechsdk
from user_input_llm_helper import AzureOpenAIHelper


class UserInputType(Enum):
    DISH = 1
    SERVINGS = 2


class UserInputHandler():

    def __init__(self, azure_openai_model):
        self.azure_openai_model = azure_openai_model
        self.azure_openai_helper = AzureOpenAIHelper(azure_openai_model)
        self.stt_key=os.environ.get('SPT_API_KEY')
        self.stt_location=os.environ.get('SPT_REGION')
        self.not_defined_language = "NOT_DEFINED"

    def clean_dish_input(self, user_input, language):
        cleaned_dish_name = self.azure_openai_helper.clean_dish_name(user_input, language)
        cleaned_dish_name_json = json.loads(cleaned_dish_name.choices[0].message.content)
        if not cleaned_dish_name_json['is_valid']:
            print("(First Check) Input does not contain a valid dish name. ")
            return None

        print("(First Check) Cleaned dish name: " + str(cleaned_dish_name_json['dish_name']))

        if not self.azure_openai_helper.does_input_type_match(cleaned_dish_name_json['dish_name'], "dish name", language):
            print("(Second Check): Input is not a real dish name.")
            return None

        return cleaned_dish_name_json['dish_name']


    def clean_servings_input(self, user_input, language):
        cleaned_servings_size = self.azure_openai_helper.clean_servings_size(user_input, language)
        cleaned_servings_size_json = json.loads(cleaned_servings_size.choices[0].message.content)

        if not cleaned_servings_size_json['is_valid']:
            print("(First Check) Input does not contain a valid servings size. ")
            return None

        print("(First Check) Cleaned servings size " + str(cleaned_servings_size_json['number_of_people']))

        if not self.azure_openai_helper.does_input_type_match(cleaned_servings_size_json['number_of_people'], "integer", language):
            print("(Second Check): Input is not a real servings size.")
            return None

        return cleaned_servings_size_json['number_of_people']


    # Return None if input is not valid, or the cleaned text/number.
    def input_cleaner(self, user_inp, language_inp, user_input_type:UserInputType):
        # Getting language of user prompt
        language = language_inp
        if language_inp is None or language_inp == self.not_defined_language:
            language = self.azure_openai_helper.ask_language(user_inp)
        print("Language is: " + language)

        if user_input_type == UserInputType.DISH:
            return self.clean_dish_input(user_inp, language)
        elif user_input_type == UserInputType.SERVINGS:
            return self.clean_servings_input(user_inp, language)
        else:
            print("Error case")
            return None


    def recognize_from_microphone(self):
        speech_recognizer = self.setup_speech_recognizer()
        scraped_values = {
            'dish_name':     self.get_input_from_user(speech_recognizer, "Tell the dish name: ", UserInputType.DISH),
            'serving_count': self.get_input_from_user(speech_recognizer, "Tell your serving size (Number of people): ", UserInputType.SERVINGS)
        }
        return scraped_values


    def setup_speech_recognizer(self):
        speech_config = speechsdk.SpeechConfig(self.stt_key, self.stt_location)
        speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "3")
        auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["en-US", "de-DE", "tr-TR"])
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            auto_detect_source_language_config=auto_detect_source_language_config,
            audio_config=audio_config)
        return speech_recognizer


    def get_input_from_user(self, speech_recognizer, message, user_input_type):
        while True:
            print(message)
            user_input = speech_recognizer.recognize_once()
            print("User entered: ", user_input.text)
            detected_language = speechsdk.AutoDetectSourceLanguageResult(user_input).language

            if user_input.reason == speechsdk.ResultReason.RecognizedSpeech:
                cleaned_input = self.input_cleaner(self.eliminate_punctuations(user_input.text), detected_language, user_input_type)
                if cleaned_input:
                    return cleaned_input
                else:
                    continue
            elif user_input.reason == speechsdk.ResultReason.Canceled:
                print("Speech input cancelled. Exiting.")
                cancellation_details = user_input.cancellation_details
                print("Speech Recognition canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")
                return None
            else:
                print("Speech is not recognized. Please try again.")
                continue


    def recognize_from_text(self):
        # while True:
        scraped_values = {}

        # Get Dish ---
        while True:
            user_input_for_dish = input("Tell the dish name:\n")
            scraped_values['dish_name'] = self.input_cleaner(self.eliminate_punctuations(user_input_for_dish), self.not_defined_language, UserInputType.DISH)
            print(scraped_values['dish_name'])
            if scraped_values['dish_name'] is not None:
                break

        # Get Count ---
        while True:
            user_input_for_count = input("Tell your count request (Number of people):\n")
            scraped_values['serving_count'] = self.input_cleaner(self.eliminate_punctuations(user_input_for_count), self.not_defined_language, UserInputType.SERVINGS)
            if scraped_values['serving_count'] is not None:
                break
        print("..............................................................")

        return scraped_values


    def eliminate_punctuations(self, user_input):
        eliminated_sentence = user_input
        characters_to_replace = [',', '.', ':', ';', '"', '\'', "?", "!"]

        # Replace specified characters with a space
        for char in characters_to_replace:
            eliminated_sentence = eliminated_sentence.replace(char, ' ')

        return eliminated_sentence