import io, os

from google.cloud import texttospeech
from playsound import playsound

def sentense_converter(not_forget_this_time, keywords, badFound, user_name):
    not_forget_message = ''
    if not_forget_this_time != []:
        not_forget_message = 'Good Work, ' + user_name + ' you didn\'t forget '
        for item in not_forget_this_time:
            not_forget_message += (item + ' ')
        not_forget_message +=  'this time'
    not_forget_this_time = []
    if keywords == []:
        output = 'Well done, ' + user_name + ' you have everything you need, have a wonderful day!'
    else:
        output = 'You have forgotten about: '
        for keyword in keywords:
            output += keyword + ', '

        if badFound:
            output += 'you dumb!'

    if not_forget_message == '':
            return output
        
    return output + " Also " + not_forget_message

def text_to_speech(sentense, language, gender):

    # get the gender parameter
    if gender == 'F':
        gender_code = texttospeech.enums.SsmlVoiceGender.FEMALE
    if gender == 'M':
        gender_code = texttospeech.enums.SsmlVoiceGender.MALE

    text_to_speech_client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.types.SynthesisInput(text=sentense)

    voice = texttospeech.types.VoiceSelectionParams(
        language_code=language,
        ssml_gender=gender_code)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    text_to_speech_response = text_to_speech_client.synthesize_speech(synthesis_input, voice, audio_config)
    # print(output)
    with open('output.mp3', 'wb') as out:
        # Write the response to the output file.
        out.write(text_to_speech_response.audio_content)
        # print('Audio content written to file "output.mp3"')
        playsound('output.mp3')
        os.remove('output.mp3')