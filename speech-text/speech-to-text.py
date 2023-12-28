import os
from openai import AzureOpenAI
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError
import azure.cognitiveservices.speech as speechsdk

# OpenAI
AZURE_OPENAI_ENDPOINT= os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY= os.getenv("AZURE_OPENAI_KEY")


# Speech-to-Text
stt_key= os.getenv("STT_KEY")
stt_location= os.getenv("STT_LOCATION")

# Translate Service
key = os.getenv("Azure_TRANSLATE_KEY")
endpoint = os.getenv("Azure_TRANSLATE_ENDPOINT")
region = os.getenv("Azure_TRANSLATE_REGION")

translate = True


def language_determine(raw_user_input):
    messages=[
        {"role": "system", "content": "You are an expert that reads user comments give answer the question."
                                      "Find the language user uses"
                                      "Return only the language name such as 'English' or 'German' etc."
                                      "Do not return anything else."
         },
        {"role": "user", "content": raw_user_input}
    ]
    openai_client = AzureOpenAI(
        api_key=AZURE_OPENAI_KEY,
        api_version="2023-12-01-preview",
        azure_endpoint = AZURE_OPENAI_ENDPOINT
    )
    response = openai_client.chat.completions.create(model="test-deployment", messages=messages)
    if(response.choices[0].message.content == "Language: Unknown." or response.choices[0].message.content[:10] == "I am sorry"):
        print("Language is Unknown.")
    else:
        language = response.choices[0].message.content
        return language


def translater(from_language, to_language, raw_user_input):
    credential = TranslatorCredential(key, region)
    text_translator = TextTranslationClient(endpoint=endpoint, credential=credential)

    try:
        target_languages = [to_language]
        input_text_elements = [InputTextItem(text=raw_user_input)]

        response = text_translator.translate(content=input_text_elements, to=target_languages, from_parameter=from_language)
        translation = response[0] if response else None
        if translation:
            for translated_text in translation.translations:
                return translated_text.text
    except HttpResponseError as exception:
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")


def azure_openai_ask(user_input):
    messages=[
        {"role": "system", "content": "You are an expert that answer user question in English"
                                      "Try to answer in only one sentence with few words."
                                      "Do not answer with only 1-2 words."
                                      "Do not give so much details."
                                      "Answer question with same language as it is."},
        {"role": "user", "content": user_input}
    ]

    openai_client = AzureOpenAI(
        api_key=AZURE_OPENAI_KEY,
        api_version="2023-12-01-preview",
        azure_endpoint =AZURE_OPENAI_ENDPOINT
    )
    response = openai_client.chat.completions.create(
        model="test-deployment",
        messages=messages
    )
    return response.choices[0].message.content


def text_to_speech(target_language, text_to_speech):
    speech_config = speechsdk.SpeechConfig(stt_key, stt_location)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    if target_language == "en":
        speech_config.speech_synthesis_voice_name='en-GB-RyanNeural'
    elif target_language == "de":
        speech_config.speech_synthesis_voice_name='de-DE-KatjaNeural'
    elif target_language == "fr":
        speech_config.speech_synthesis_voice_name='fr-FR-DeniseNeural'
    elif target_language == "es":
        speech_config.speech_synthesis_voice_name='es-ES-AlvaroNeural'
    elif target_language == "tr":
        speech_config.speech_synthesis_voice_name='tr-TR-AhmetNeural'
    else:
        speech_config.speech_synthesis_voice_name='en-US-JennyNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text_to_speech).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text_to_speech))
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
    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["en-US", "de-DE", "fr-FR", "tr-TR"])
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
            print("Question: ", user_input.text)
            print("Question Language: ", detected_language)

            if translate:
                response_to_user_input = azure_openai_ask(user_input.text)
                print("Response to user input: ", response_to_user_input)

                text_to_speech(detected_language[:2], response_to_user_input)

            else:
                # user_input_language = language_determine(user_input.text) # 'speech_recognizer' determines the language

                english_user_input = translater(detected_language[:2], "en", user_input.text)
                print("English version of user input: ", english_user_input)
                if english_user_input == "Exit.":
                    break

                response_to_user_input = azure_openai_ask(english_user_input)
                print("Response to user input: ", response_to_user_input)

                translated_response_to_user_input = translater("en", detected_language[:2], response_to_user_input)
                print("Translation is used:")
                print("Translated to native language, user response: ", translated_response_to_user_input)

                text_to_speech(detected_language[:2], translated_response_to_user_input)

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