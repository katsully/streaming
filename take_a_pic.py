from io import BytesIO
from google.cloud import storage
import cv2  
import time  
from PIL import Image  
import numpy as np  
import os  

# Folder  
folder = "frames"  

# Create the frames folder if it doesn't exist  
frames_dir = os.path.join(os.getcwd(), folder)  
os.makedirs(frames_dir, exist_ok=True)  

def take_image():
    # Initialize the webcam  
    cap = cv2.VideoCapture(0)  

    # Check if the webcam is opened correctly  
    if not cap.isOpened():  
        raise IOError("Cannot open webcam")  

    # Wait for the camera to initialize and adjust light levels  
    time.sleep(5)  

    ret, frame = cap.read()  
    if ret:  
        # Convert the frame to a PIL image  
        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))  

        # Resize the image  
        max_size = 250  
        ratio = max_size / max(pil_img.size)  
        new_size = tuple([int(x*ratio) for x in pil_img.size])  
        resized_img = pil_img.resize(new_size, Image.LANCZOS)  

        # Convert the PIL image back to an OpenCV image  
        frame = cv2.cvtColor(np.array(resized_img), cv2.COLOR_RGB2BGR)  

        # Save the frame as an image file  
        path = f"{folder}/frame.jpg"  
        cv2.imwrite(path, frame)  
    else:  
        print("Failed to capture image")  


    # Release the camera and close all windows  
    cap.release()  
    cv2.destroyAllWindows()  
      
    # connect to your google storage account
    storage_client = storage.Client.from_service_account_json("gemini-testing.json", project='Gemini-Testing')

    # select your bucket
    bucket = storage_client.get_bucket("hex-test-bucket2")

    # where we are grabbing the image we just took in the code above
    path = "frames/frame.jpg"

    # set up the path where we are uploading the image in the image
    blob = bucket.blob("images/{}.jpg".format("frame"))

    blob.content_type = "image/jpeg"

    # upload the image to the bucket
    with open(path, 'rb') as f:
        blob.upload_from_file(f)

