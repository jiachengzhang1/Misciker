from __future__ import division

import io, os
import re
import sys

import pyaudio
import geocoder
from travelEstimater import get_time_estimation
from time import sleep
from time import localtime
from time import strftime
import datetime as dt
from textToSpeech import text_to_speech
from textToSpeech import sentense_converter
from keyword_finder import findKeyword

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from six.moves import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

past_forgotten_items = []

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)

def listen_respond_loop(responses, check_list, user_name, language_code, gender, address, estimate_time):
    global past_forgotten_items
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """

    num_chars_printed = 0
    output = ''
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            output =  output + '\n' + transcript
            output = output.lower()
            print(transcript + overwrite_chars)
            if transcript.lower().find('good morning') != -1:
                t = localtime()
                current_time = strftime("%H:%M", t)
                text_to_speech('Good morning ' + user_name + ' now is '+current_time+', it takes ' + estimate_time + ' travel to ' + address, language_code, gender)
                sleep(0.05)

            # if transcript.lower().find('hello google') != -1:
            #     output = ''

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if transcript.lower().find('hello google') != -1 and re.search(r'\b(missing|missed)\b', transcript.lower(), re.I):
                forgottenItems, badFound = findKeyword(output, ['freaking', 'stupid'], check_list)

                # reset not_forget_this_time
                not_forget_this_time = []

                # if have past forgotten items, check if they are included this time
                if past_forgotten_items != []:
                    for past_forgotten_item in past_forgotten_items:
                        if output.find(past_forgotten_item) != -1:
                            not_forget_this_time.append(past_forgotten_item)

                # update the past_forgotten_items, since the items forgot this time is changed
                past_forgotten_items = []
                if forgottenItems != []:
                    for forgottenItem in forgottenItems:
                        past_forgotten_items.append(forgottenItem)      
                
                text_to_speech(sentense_converter(not_forget_this_time, 
                                                  forgottenItems, 
                                                  badFound, 
                                                  user_name), 
                                language_code, 
                                gender)
                output = ''
                num_chars_printed = 0
                break

            num_chars_printed = 0


def startSpeechDetector(user_name, check_list, language_code, gender, address):
    speech_to_text_client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    text_to_speech("Well Done" + user_name + ", new you are all set!, Just tell me the items you are carrying out when you leave the house, I'll remind you the forgotten items. Enjoy!", language_code, gender)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        speech_to_text_responses = speech_to_text_client.streaming_recognize(streaming_config, requests)
        # Now, put the transcription responses to use.
        while True:
            location = geocoder.ip('me')
            latlng_string = str(location.latlng[0]) + ', ' + str(location.latlng[1])
            estimate_time = get_time_estimation(latlng_string, address)
            listen_respond_loop(speech_to_text_responses, check_list, user_name, language_code, gender, address, estimate_time)
            sleep(0.05)
    





