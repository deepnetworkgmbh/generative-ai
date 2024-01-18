import os

import azure.cognitiveservices.speech as speechsdk


def create_speech_recognizer():
    stt_key = os.environ.get('SPT_API_KEY')
    stt_location = os.environ.get('SPT_REGION')

    speech_config = speechsdk.SpeechConfig(stt_key, stt_location)
    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
        languages=["en-US", "de-DE", "tr-TR"])
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        auto_detect_source_language_config=auto_detect_source_language_config,
        audio_config=audio_config)
    return speech_recognizer
