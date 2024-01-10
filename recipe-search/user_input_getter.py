import json

import azure.cognitiveservices.speech as speechsdk
from openai_ask import openai_ask_dish_init
from openai_ask import openai_ask_language
from openai_ask import openai_ask_general_check
from openai_ask import openai_ask_count_init

# Speech-to-Text
stt_key='05e0d71cfca242cbaa7117d138f394ff'
stt_location='germanywestcentral'


def input_handler(user_inp, language_inp, dish_or_count):
    # Getting language of user prompt
    language = language_inp
    if language_inp == "NOT_DEFINED":
        language = openai_ask_language(user_inp)
    print("Used Language is: " + language)

    # Scraping dish/count value
    if dish_or_count == "dish":
        openai_answer_for_dish_init = openai_ask_dish_init(user_inp, language)
        openai_answer_for_dish_init_json = json.loads(openai_answer_for_dish_init.choices[0].message.content)
        print("Input value: " + str(openai_answer_for_dish_init_json['dish_name']))
        print("(First Check) If given value is dish or not: " + str(openai_answer_for_dish_init_json['is_dish']))

        if openai_answer_for_dish_init_json['is_dish']:
            openai_answer_for_dish_general = openai_ask_general_check(openai_answer_for_dish_init_json['dish_name'], "dish name", language)
            openai_answer_general_for_dish_json = json.loads(openai_answer_for_dish_general.choices[0].message.content)
            print("(Second Check) If given value is dish or not: " + openai_answer_general_for_dish_json['is_that_type'])
            return openai_answer_for_dish_init_json['dish_name']
        else:
            return None
    elif dish_or_count == "count":
        openai_answer_for_count_init = openai_ask_count_init(user_inp, language)
        openai_answer_for_count_init_json = json.loads(openai_answer_for_count_init.choices[0].message.content)
        print("Input value: " + str(openai_answer_for_count_init_json['number_of_people']))
        print("(First Check) If given value is serving count or not: " + str(openai_answer_for_count_init_json['is_count']))

        if openai_answer_for_count_init_json['is_count']:
            print(openai_answer_for_count_init_json['number_of_people'])
            print(language)
            openai_answer_for_count_general = openai_ask_general_check(openai_answer_for_count_init_json['number_of_people'], "integer", language)
            openai_answer_general_for_count_json = json.loads(openai_answer_for_count_general.choices[0].message.content)
            print("(Second Check) If given value is serving count or not: " + openai_answer_general_for_count_json['is_that_type'])
            return openai_answer_for_count_init_json['number_of_people']
        else:
            return None
    else:
        print("Error case")
        return None


def recognize_from_microphone():
    speech_config = speechsdk.SpeechConfig(stt_key, stt_location)
    speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "10")
    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["en-UK", "de-DE", "tr-TR"])
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        auto_detect_source_language_config=auto_detect_source_language_config,
        audio_config=audio_config)

    while True:
        scraped_values = {}

        print("Tell the dish name): ")
        user_input_for_dish = speech_recognizer.recognize_once()
        auto_detect_source_language_result_for_dish = speechsdk.AutoDetectSourceLanguageResult(user_input_for_dish)
        detected_language_for_dish = auto_detect_source_language_result_for_dish.language

        # Get Dish ---
        if user_input_for_dish.reason == speechsdk.ResultReason.RecognizedSpeech:
            scraped_values['dish_name'] =  input_handler(user_input_for_dish, detected_language_for_dish, "dish")
        else:
            print("Speech error.")
            print("Did you set the speech resource key and region values?")

        # ---------------------------------------------------------------------------------------------------------
        # Get Count ---
        print("Tell your serving count request (Number of people): ")
        user_input_for_count = speech_recognizer.recognize_once()
        auto_detect_source_language_result_for_count = speechsdk.AutoDetectSourceLanguageResult(user_input_for_count)
        detected_language_for_count = auto_detect_source_language_result_for_count.language

        if user_input_for_count.reason == speechsdk.ResultReason.RecognizedSpeech:
            scraped_values['serving_count'] =  input_handler(user_input_for_count, detected_language_for_count, "count")
        else:
            print("Speech error.")
            print("Did you set the speech resource key and region values?")
        print("..............................................................")
        return scraped_values

def recognize_from_text():
    # while True:
    scraped_values = {}

    # Get Dish ---
    user_input_for_dish = input("Tell the dish name:\n")
    scraped_values['dish_name'] = input_handler(user_input_for_dish, "NOT_DEFINED", "dish")

    # Get Count ---
    user_input_for_count = input("Tell your count request (Number of people):\n")
    scraped_values['serving_count'] = input_handler(user_input_for_count, "NOT_DEFINED", "count")
    print("..............................................................")

    return scraped_values