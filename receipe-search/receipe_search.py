import json
import os
from openai import AzureOpenAI
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError
import azure.cognitiveservices.speech as speechsdk

# OpenAI
AZURE_OPENAI_ENDPOINT='https://openai-dn.openai.azure.com/'
AZURE_OPENAI_KEY='44d2c6a693354551bddeb90429201899'


# Speech-to-Text
stt_key='05e0d71cfca242cbaa7117d138f394ff'
stt_location='germanywestcentral'

# Translate Service
key = "61e121063c40410fb33dd78f35e8f9ce"
endpoint = "https://api.cognitive.microsofttranslator.com/"
region = "westeurope"


def food_name_getter(user_request):

    parameters_schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": 'The name of the meal. If no name is provided, return "not_stated".',
            },
        },
        "required": ["name"],
    }

    function_schema = {
        "name": "get_meal_name",
        "description": "Get/Scrape meal name from the statement.",
        "parameters": parameters_schema,
    }

    messages= [{"role": "system", "content": "You are an assistant that gets food name from the statement."
                                             "Give only the food/meal name."
                                             "Do not give other information."
                                             "Do not give instructions or ingredients."
                }, {"role": "user", "content": user_request}]

    client = AzureOpenAI(
        azure_endpoint='https://openai-dn-fr.openai.azure.com/',
        api_key='533bb10c9d82416e8731e493104eed3e',
        api_version="2023-09-01-preview"
    )

    response = client.chat.completions.create(
        model='test-deployment',
        messages=messages,
        functions=[function_schema],
        function_call={"name": function_schema["name"]},
    )

    args = json.loads(response.choices[0].message.function_call.arguments)
    return args

def ask_to_user(user_request):

    speech_config = speechsdk.SpeechConfig(stt_key, stt_location)
    speech_config.speech_synthesis_voice_name='en-GB-RyanNeural'
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(user_request).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(user_request))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")


def recognize_from_microphone():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(stt_key, stt_location)
    speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "10")
    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["en-US", "de-DE"])
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        auto_detect_source_language_config=auto_detect_source_language_config,
        audio_config=audio_config)

    while True:
        print("Please speak...")
        user_input = speech_recognizer.recognize_once()
        auto_detect_source_language_result = speechsdk.AutoDetectSourceLanguageResult(user_input)
        detected_language = auto_detect_source_language_result.language

        if user_input.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("User Request: ", user_input.text)
            print("User Request Language: ", detected_language)

            returned_args = food_name_getter(user_input.text)
            print(returned_args)


            # print("food Name: ", food_name)
            #
            # ask_to_user(food_name)
            #
            # print("Please say 'yes' or 'no'...")
            # yes_or_no = speech_recognizer.recognize_once()
            # print(yes_or_no.text)
            #
            # if yes_or_no.text == "Yes.":
            #     print("Success")
            # else:
            #     continue

            print("..............................................................")
        elif user_input.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(user_input.no_match_details))
        elif user_input.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = user_input.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
    print("Goodbye")

recognize_from_microphone()