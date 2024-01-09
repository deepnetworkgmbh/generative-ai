import json

import azure.cognitiveservices.speech as speechsdk
from openai_ask import openai_ask_meal_init
from openai_ask import openai_ask_meal_check
from openai_ask import openai_ask_language
from openai_ask import openai_ask_general_check
from openai_ask import openai_ask_count_init
from speaker_ask import ask_to_user

# Speech-to-Text
stt_key='05e0d71cfca242cbaa7117d138f394ff'
stt_location='germanywestcentral'

def input_handler(user_inp, language_inp, meal_or_count):
    # Getting language of user prompt
    language = language_inp
    if language_inp == "NOT_DEFINED":
        language = openai_ask_language(user_inp)

    # Scraping meal/count value
    if meal_or_count == "meal":
        openai_answer_for_meal_init = openai_ask_meal_init(user_inp, language)
        openai_answer_for_meal_init_json = json.loads(openai_answer_for_meal_init.choices[0].message.content)
        print("Input value: " + user_inp)
        print("If given value is meal/food or not: " + str(openai_answer_for_meal_init_json['is_meal']))

        if openai_answer_for_meal_init_json['is_meal']:
            openai_answer_for_meal_general = openai_ask_general_check(openai_answer_for_meal_init_json['meal_name'], "dish name", language)
            openai_answer_general_for_meal_json = json.loads(openai_answer_for_meal_general.choices[0].message.content)
            print("Result of the double check: " + openai_answer_general_for_meal_json['is_that_type'])
    elif meal_or_count == "count":
        openai_answer_for_count_init = openai_ask_meal_init(user_inp, language)
        openai_answer_for_count_init_json = json.loads(openai_answer_for_count_init.choices[0].message.content)
        print("Input value: " + user_inp)
        print("If given value is meal/food or not: " + str(openai_answer_for_count_init_json['is_count']))

        if openai_answer_for_count_init_json['is_meal']:
            openai_answer_for_count_general = openai_ask_general_check(openai_answer_for_count_init_json['number_of_people'], "integer", language)
            openai_answer_general_for_count_json = json.loads(openai_answer_for_count_general.choices[0].message.content)
            print("Result of the double check: " + openai_answer_general_for_count_json['is_that_type'])
    else:
        print("Error case")


def recognize_from_microphone():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(stt_key, stt_location)
    speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "10")
    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["en-UK", "de-DE", "tr-TR"])
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        auto_detect_source_language_config=auto_detect_source_language_config,
        audio_config=audio_config)

    while True:
        print("Tell your meal request (Meal name): ")
        user_input_for_meal = speech_recognizer.recognize_once()
        auto_detect_source_language_result_for_meal = speechsdk.AutoDetectSourceLanguageResult(user_input_for_meal)
        detected_language_for_meal = auto_detect_source_language_result_for_meal.language

        # Get Meal ---
        if user_input_for_meal.reason == speechsdk.ResultReason.RecognizedSpeech:
            input_handler(user_input_for_meal, detected_language_for_meal, "meal")
        else:
            print("Speech error.")
            print("Did you set the speech resource key and region values?")

        # ---------------------------------------------------------------------------------------------------------
        # Get Count ---
        print("Tell your count request (Number of people): ")
        user_input_for_count = speech_recognizer.recognize_once()
        auto_detect_source_language_result_for_count = speechsdk.AutoDetectSourceLanguageResult(user_input_for_count)
        detected_language_for_count = auto_detect_source_language_result_for_count.language

        if user_input_for_count.reason == speechsdk.ResultReason.RecognizedSpeech:
            input_handler(user_input_for_count, detected_language_for_count, "count")
        else:
            print("Speech error.")
            print("Did you set the speech resource key and region values?")
        print("..............................................................")


def recognize_from_text():
    while True:
        # Get Meal ---
        user_input_for_meal = input("Tell your meal request (Meal name):\n")
        input_handler(user_input_for_meal, "NOT_DEFINED", "meal")

        # Get Count ---
        user_input_for_count = input("Tell your count request (Number of people):\n")
        input_handler(user_input_for_count, "NOT_DEFINED", "count")
        print("..............................................................")
