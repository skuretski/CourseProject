import base64
import json
import os

from google.cloud import storage
from google.cloud import vision
from dotenv import load_dotenv

load_dotenv()

visionClient = vision.ImageAnnotatorClient()
storageClient = storage.Client()
projectId = os.environ["GCP_PROJECT"]

print(projectId)

def process_image(file, context):
	bucket = validate_message(file, "bucket")
	name = validate_message(file, "name")

	detect_text(bucket, name)