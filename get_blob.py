from google.cloud import storage

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