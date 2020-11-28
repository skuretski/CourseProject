from __future__ import print_function
import base64
import json
import os
import sys

from google.cloud import storage
from google.cloud import vision
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv

load_dotenv()

visionClient = vision.ImageAnnotatorClient()
storageClient = storage.Client()
translateClient = translate.Client()
projectId = os.environ["GCP_PROJECT"]
bucket = storageClient.get_bucket('cs410_images')
resultBucket = storageClient.get_bucket('cs410_ocr_results')

def process_images():

	for file in storageClient.list_blobs(bucket):
		image = vision.Image(
			source=vision.ImageSource(gcs_image_uri=f"gs://cs410_images/{file.name}")
		)
		text_detection_response = visionClient.text_detection(image=image)
		annotations = text_detection_response.text_annotations
		if len(annotations) > 0:
			text = annotations[0].description
		else:
			text = ""
		detect_language_response = translateClient.detect_language(text)
		src_lang = detect_language_response["language"]

		if text != "" and text is not None and src_lang == "en":
			data = {
				"src_lang": src_lang,
				"text": text,
				"file_name": file.name,
				"id": file.name.split(".")[0]
			}

			filename = file.name.split(".")[0] + '.json'

			with open("data/" + filename, 'w', encoding="utf-8") as outfile:
				json.dump(data, outfile)
			blob = resultBucket.blob(filename)

			with open('data/' + filename, 'rb') as f:
				blob.upload_from_file(f)

process_images()
