from google.cloud import storage
from openai import AzureOpenAI
import os

# client is a variable that represents the 'bridge' for how our code
# will connect with OpenAI
client = AzureOpenAI(
	azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT'),
	api_key = os.getenv('AZURE_OPENAI_KEY'),
	api_version = '2023-12-01-preview'
)

# getting the list of labels from our google storage bucket
def get_list():
	storage_client = storage.Client.from_service_account_json("gemini-testing.json", project='Gemini-Testing')

	bucket = storage_client.get_bucket("hex-test-bucket2")

	# select the file from your storage bucket
	blob = bucket.blob("cta_test/data.txt")
	# because we are overwriting an exisiting file, we need to get
	# the latest version - reload ensures this
	blob.reload()
	# download the text file to this local repository
	blob = blob.download_as_string()
	blob = blob.decode('utf-8')
	return blob

# using the labels from our google storage bucket, and openAI chat
# describe the scene via the camera
def describe_scene():
	our_labels = get_list()

	my_messages = [
		{'role': 'system', 'content': 'You are Rob Reilly, CCO of WPP, the largest advertising company and most creative company. You are a New Yorker, funny, and a bit snarky.'},
		{'role': 'user', 'content': 'Describe the scene in front of you. To help understand the world in front of you, here are some objects in the scene {} Keep it short.'.format(our_labels)}
	]

	response = client.chat.completions.create(
		model = "GPT-4",
		messages = my_messages
	)

	return response.choices[0].message.content