from take_a_pic import take_image
from get_blob import get_list
from streaming_utils import create_audio
from test_client import main
import time

# take an image and upload it to the Google storage bucket
take_image()
# wait a bit more pulling the txt file from Google cloud
time.sleep(10)
print('done sleeping')
# get the list of labels from google cloud
my_list = get_list()
print(my_list)
# create a wav file based on the downloaded list of labels
create_audio(my_list)
# send the created wav file to Omniverse
main('output.wav', '/World/audio2face/PlayerStreaming')