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
        print("Tell your request: ")
        user_input_for_meal = speech_recognizer.recognize_once()
        auto_detect_source_language_result_for_meal = speechsdk.AutoDetectSourceLanguageResult(user_input_for_meal)
        detected_language_for_meal = auto_detect_source_language_result_for_meal.language

        # Get Meal ---
        if user_input_for_meal.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Language: " + detected_language_for_meal)
            openai_answer_for_meal_init = openai_ask_meal_init(user_input_for_meal, detected_language_for_meal)
            openai_answer_for_meal_init_json = json.loads(openai_answer_for_meal_init.choices[0].message.content)
            print("Input value: " + user_input_for_meal)
            print("If given value is meal/food or not: " + str(openai_answer_for_meal_init_json['is_meal']))

            if openai_answer_for_meal_init_json['is_meal']:
                openai_answer_for_meal_general = openai_ask_general_check(openai_answer_for_meal_init_json['meal_name'], "dish name", user_input_for_meal_language)
                openai_answer_general_for_meal_json = json.loads(openai_answer_for_meal_general.choices[0].message.content)
                print("Result of the double check: " + openai_answer_general_for_meal_json['is_that_type'])
        else:
            print("Speeh error.")
            print("Did you set the speech resource key and region values?")

        # Get Count ---
        user_input_for_count = speech_recognizer.recognize_once()
        auto_detect_source_language_result_for_meal = speechsdk.AutoDetectSourceLanguageResult(user_input_for_meal)
        detected_language_for_meal = auto_detect_source_language_result_for_meal.language

        if user_input_for_count.reason == speechsdk.ResultReason.RecognizedSpeech:
            openai_answer_for_count_init = openai_ask_count_init(user_input_for_count, detected_language_for_meal)
            openai_answer_for_count_init_json = json.loads(openai_answer_for_count_init.choices[0].message.content)
            print("Input value: " + user_input_for_count)
            print("If given value is valid count or not: " + str(openai_answer_for_count_init_json['is_count']))

            if openai_answer_for_count_init_json['is_count']:
                openai_answer_general = openai_ask_general_check(str(openai_answer_for_count_init_json['number_of_people']), "integer", user_input_for_count_language)
                openai_answer_general_json = json.loads(openai_answer_general.choices[0].message.content)
                print("Result of the double check: " + openai_answer_general_json['is_that_type'])
        print("..............................................................")


def recognize_from_text():
    while True:
        # Get Meal ---
        user_input_for_meal = input("Tell me the dish name: \n")
        user_input_for_meal_language = openai_ask_language(user_input_for_meal)
        print("Language: " + user_input_for_meal_language)
        openai_answer_for_meal_init = openai_ask_meal_init(user_input_for_meal, user_input_for_meal_language)
        openai_answer_for_meal_init_json = json.loads(openai_answer_for_meal_init.choices[0].message.content)
        print("Input value: " + user_input_for_meal)
        print("If given value is meal/food or not: " + str(openai_answer_for_meal_init_json['is_meal']))

        if openai_answer_for_meal_init_json['is_meal']:
            openai_answer_for_meal_general = openai_ask_general_check(openai_answer_for_meal_init_json['meal_name'], "dish name", user_input_for_meal_language)
            openai_answer_general_for_meal_json = json.loads(openai_answer_for_meal_general.choices[0].message.content)
            print("Result of the double check: " + openai_answer_general_for_meal_json['is_that_type'])

        # Get Count ---
        user_input_for_count = input("Tell me the number of people: \n")
        user_input_for_count_language = openai_ask_language(user_input_for_count)
        openai_answer_for_count_init = openai_ask_count_init(user_input_for_count, user_input_for_count_language)
        openai_answer_for_count_init_json = json.loads(openai_answer_for_count_init.choices[0].message.content)
        print("Input value: " + user_input_for_count)
        print("If given value is valid count or not: " + str(openai_answer_for_count_init_json['is_count']))

        if openai_answer_for_count_init_json['is_count']:
            openai_answer_general = openai_ask_general_check(str(openai_answer_for_count_init_json['number_of_people']), "integer", user_input_for_count_language)
            openai_answer_general_json = json.loads(openai_answer_general.choices[0].message.content)
            print("Result of the double check: " + openai_answer_general_json['is_that_type'])
        print("..............................................................")

