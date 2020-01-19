import io, os
from speechToText import startSpeechDetector
from appConfig import getConfig

user_name = 'testing'
input_language_code = 'en-us'
language_code = 'en_au'
gender = 'F'
check_list = ['wallet','keys', 'phone', 'backpack']

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"GoogleVision.json"

user_name, check_list, language_code, gender, address = getConfig()

startSpeechDetector(user_name, check_list, language_code, gender, address)
