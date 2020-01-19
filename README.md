# Misciker

### Description
This is a Morning Sanity Checker!

Misciker (Morning Sanity Checker) is an app that utilizes Google Clouds Voice API's and Map Matrix API 
to inform you of your morning commute time to work and prevents you from forgetting
your daily items that you take for that day. 

It sets up by asking for your name, where you work, preferences for the assistants voice and your morning items check list.

After that there are two voice controls
"Good morning Misciker": Notifying you of the travel time to work for that day, accounting for incidents along the route
as it uses Google's Map distance matrix API 

"Hello Google ... missing/missed/miss ..." (A sentence beginning with "hello google" and containing missing, missed or miss as key words):  
Start a query of items that you will take for that day
After saying "Hello Google", you may start listing off items to take for the day
We currently have a reasonably sized set of common items people may take for their day
That range from their Coffee to their ID's with lanyard 

Example:
Hello Google, I would like to take my iPhone, water bottle, backpack, sunglasses, and wallet today, am I missing anything?
Then the Misciker will tell you which items are missing based on your configured morning check list and your voice command.

### Google Cloud Setup
Make sure you have a Google Cloud account created APIs enabled, see details in the links below,<br/>

##### Speech to text API:
https://cloud.google.com/speech-to-text/docs/

##### Text to speech API:
https://cloud.google.com/text-to-speech/docs/

##### Distance Matrix API:
https://developers.google.com/maps/documentation/distance-matrix/start?hl=en_US


### Setup and Run (For Mac users)
1. Create a Python virtual environment
`python3 -m venv /path/to/new/virtual/environment`

2. Activation
`source /path/to/new/virtual/environment/bin/activate`

3. Clone the project to the virtual environment

4. Install APIs and Libraries<br/>
install google cloud speech API<br/>
`pip install --upgrade google-cloud-speech`<br/><br/>
google cloud text to speech API<br/>
`pip install --upgrade google-cloud-texttospeech`<br/><br/>
pyaudio libraries<br/>
`brew install portaudio`
`pip install pyaudio`<br/>
`pip install playsound`<br/>
`pip install pyobjc`<br/>

5. Run the Application
`python launch.py`
