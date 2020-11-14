from __future__ import print_function
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
image.source.image_uri = 'gs://cs410_images/memes/2dxg4j.jpg'

process_image(image.source)

print(projectId)

def process_image(file, context):
	bucket = validate_message(file, "bucket")
	name = validate_message(file, "name")

	detect_text(bucket, name)

def detect_text(bucket, filename):
	image = vision.Image(
		source=vision.ImageSource(gcs_image_uri=f"gs://{bucket}/{filename}")
	)
	text_detection_response = vision_client.text_detection(image=image)
	annotations = text_detection_response.text_annotations
	if len(annotations) > 0:
		text = annotations[0].description
	else:
		text = NULL

	print(text)