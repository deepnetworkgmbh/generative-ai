import os
import openai
import azure.cognitiveservices.speech as speechsdk

# OpenAI
openai.api_key = '44d2c6a693354551bddeb90429201899'
openai.api_base = 'https://openai-dn.openai.azure.com/'
openai.api_type = 'azure'
openai.api_version = '2023-05-15' # this might change in the future

# Speech-to-Text
stt_key='05e0d71cfca242cbaa7117d138f394ff'
stt_location='germanywestcentral'

def recognize_from_microphone():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(stt_key, stt_location)
    speech_config.speech_recognition_language="en-US"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Our question: ", speech_recognition_result.text, " only with 10 words.")
        response = openai.Completion.create(engine="test-deployment", prompt=speech_recognition_result.text, max_tokens=10)
        text_response = response['choices'][0]['text'] # response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()
        print(text_response)

    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

recognize_from_microphone()