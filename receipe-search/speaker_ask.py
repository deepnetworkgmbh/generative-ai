import azure.cognitiveservices.speech as speechsdk

# Speech-to-Text
stt_key='05e0d71cfca242cbaa7117d138f394ff'
stt_location='germanywestcentral'


def ask_to_user(meal_name, language, text_or_audio):
    if text_or_audio == 1:
        if language == "English":
            user_request_check = input("Is your meal " + meal_name + " ? (Y/N)\n")
            if user_request_check == "Y":
                return True
            else:
                return False
        elif language == "German":
            user_request_check = input("Ist " + meal_name + " das Sie suchen? (J/N)\n")
            if user_request_check == "J":
                return True
            else:
                return False
        else:
            user_request_check = input("Aradiginiz yemek " + meal_name + " mi? (E/H)\n")
            if user_request_check == "E":
                return True
            else:
                return False
    else:
        # Asking to the user ---------------------
        speech_config = speechsdk.SpeechConfig(stt_key, stt_location)
        question_to_the_user = ""
        if language == "English":
            question_to_the_user = "Is your meal " + meal_name + " ? (Y/N)"
            speech_config.speech_synthesis_voice_name='en-GB-RyanNeural'
        elif language == "German":
            question_to_the_user = "Ist " + meal_name + " das Sie suchen? (J/N)"
            speech_config.speech_synthesis_voice_name='de-DE-ConradNeural'
        else:
            question_to_the_user = "Aradiginiz yemek " + meal_name + " mi? (E/H)"
            speech_config.speech_synthesis_voice_name='tr-TR-AhmetNeural'

        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        speech_synthesis_result = speech_synthesizer.speak_text_async(question_to_the_user).get()

        if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(meal_name))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")

        # Getting response from the user ------------------
        # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
        speech_config = speechsdk.SpeechConfig(stt_key, stt_location)
        speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "1")
        auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["en-UK", "de-DE", "tr-TR"])
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            auto_detect_source_language_config=auto_detect_source_language_config,
            audio_config=audio_config)


        user_answer = speech_recognizer.recognize_once()
        auto_detect_source_language_result = speechsdk.AutoDetectSourceLanguageResult(user_answer)
        detected_language = auto_detect_source_language_result.language

        if user_answer.reason == speechsdk.ResultReason.RecognizedSpeech:
            if (detected_language == "English" and user_answer == "Yes.") or (detected_language == "German" and user_answer == "Ja.") or (detected_language == "Turkish" and user_answer == "Evet."):
                return True
            else:
                return False
        elif user_answer.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(user_answer.no_match_details))
        elif user_answer.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = user_answer.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
