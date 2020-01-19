
import io, os, sys

import speechToText

from textToSpeech import text_to_speech

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

def listen(responses):
    num_chars_printed = 0
    # output = ''
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            return transcript

        num_chars_printed = 0


def getConfig():

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code='en_us')
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with speechToText.MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # default values
        user_name = ''
        address = ''
        check_list = []
        language_code = 'en_au'
        gender = 'F'

        # user's name
        text_to_speech("Hello, I am your morning sanity checker, Misciker. I'm here in case you forget something. Let's get started with some settings.", language_code, gender)
        text_to_speech("What's your name?", language_code, gender)
        transcript = listen(responses)
        user_name = transcript.lower().split()[-1]
        print(user_name)
        text_to_speech("Nice to meet you, " + user_name + 
                        ". Do you know you can not only change my voice type and also my accent? It is all up to you. What type of accent do you want me to speak?", 
                        language_code, gender)

        # accent choice
        language_code = ''
        count = 0
        while language_code == '':
            transcript = listen(responses)
            accent = transcript.lower()
            if accent.find('british') != -1:
                language_code = 'en-gb'
            elif accent.find('america') != -1:
                language_code = 'en-us'
            elif accent.find('india') != -1:
                language_code = 'en-in'
            elif accent.find('austrilia') != -1:
                language_code = 'en-au'
            else:
                if count == 2:
                    text_to_speech('I don\'t understand that, can you repeat that?', language_code, gender)
                    count = 0
                count += 1
        print(language_code)

        # voice type
        text_to_speech("Great! Nice choice!", language_code, gender)
        text_to_speech("Since I am your personal smart reminder, you can custmize my voice type. Which gender do you prefer?", language_code, gender)
        gender = ''
        count = 0
        while gender == '':
            transcript = listen(responses)
            gender_string = transcript.lower()
            if gender_string.lower().find('female'):
                gender = 'F'
            elif gender_string.lower().find('male'):
                gender = 'M'
            else:
                if count == 2:
                    text_to_speech('I don\'t understand that, can you repeat that?', language_code, gender)
                    count = 0
                count += 1
        print(gender)

        # address
        text_to_speech('Well done! ' + user_name + ' ,could I have your work address? You can type in the concole.', language_code, gender)
        address = input('work address:   ')
        print(address)

        # checklist
        text_to_speech("Awesome! " + user_name + ", now we are talking! You can include as many items as you want into your checklist, so that I can remind you what items you have forgot to carry before you leave the house everytime.  What items do you want to add into your checklist?", language_code, gender)
        check_list_string = input('checklist, seperate use white space:   ')
        check_list = check_list_string.split()
        print(check_list)

        return user_name, check_list, language_code, gender, address





