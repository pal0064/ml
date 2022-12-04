
import os
from gtts import gTTS

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

# Convert text to audio

def get_polly_client():
  os.environ["AWS_CONFIG_FILE"] = "/aws_credentials"
  session = Session(profile_name="default")
  polly = session.client("polly",region_name='us-east-1')
  return polly

def save_polly_response_to_file(response):
  # Access the audio stream from the response
  if "AudioStream" in response:
          with closing(response["AudioStream"]) as stream:
            output = os.path.join(gettempdir(), "speech.mp3")
            try:
              # Open a file for writing the output as a binary stream
                  with open(output, "wb") as file:
                    file.write(stream.read())
                  return output
            except IOError as error:
                print(error)
  else:
      # The response didn't contain audio data
      print("Could not stream audio")
def convert_to_audio_using_aws_polly(text,voice_id='Justin'):
  polly = get_polly_client()
  try:
      # Request speech synthesis
      response = polly.synthesize_speech(Text=text, OutputFormat="mp3",
                                          VoiceId=voice_id)
      file_name = save_polly_response_to_file(response)
  except (BotoCoreError, ClientError) as error:
      # The service returned an error, exit gracefully
      print(error)
  return file_name

def convert_to_audio_using_gtts(text):
  tts = gTTS(text,lang='en',slow=True)
  file_name='1.wav' 
  tts.save(file_name)
  return file_name

def convert_to_audio(words,engine_type='gtts'):
  if engine_type=='gtts':
      return convert_to_audio_using_gtts(" ".join(words))
  elif engine_type=='polly':
      return convert_to_audio_using_aws_polly(" ".join(words))