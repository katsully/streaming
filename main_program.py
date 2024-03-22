from take_a_pic import take_image
from description_creator import describe_scene
from streaming_utils import create_audio
from test_client import main
import time

# take an image and upload it to the Google storage bucket
take_image()
# wait a bit more pulling the txt file from Google cloud
time.sleep(10)
print('done sleeping')
# get the list of labels from google cloud
scene_description = describe_scene()
print(scene_description)
# create a wav file based on the downloaded list of labels
create_audio(scene_description)
# send the created wav file to Omniverse
main('output.wav', '/World/audio2face/PlayerStreaming')