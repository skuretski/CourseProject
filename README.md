# CS410 Fall 2020 Course Project
Written by Susie Kuretski (skure2@illinois.edu)

# Topic
Utilizing Google Vision's optical character recognition to perform K-means cluster analysis

# Overview
From this [Kaggle](https://www.kaggle.com/sayangoswami/reddit-memes-dataset) dataset, which includes data for ~3300 Reddit memes, I extracted the images and uploaded them to a Google Cloud Platform storage bucket. Then, I ran these images through optical character recognition and translation using Google Vision and Translate. Link to API docs [here](https://cloud.google.com/vision/docs/ocr). Once this was done, the results were stored in a GCP bucket as JSON data. An example would be:

## The starting image

![85805u](https://github.com/skuretski/CourseProject/blob/main/85805u.jpg?raw=true "85805u")

## The JSON result after OCR

`{` <br />
`"src_lang": "en",`<br/>
`"text": "When you don't study for a test\nand get all the answers right\nSo this is the power of Ultra Instinct?\n",`<br/> 
`"file_name": "85805u.jpg",`<br/> 
`"id": "85805u"`<br/>
`}`

**The goal after this was to perform K-means cluster analysis to discover groups or common themes in the memes.**

# Step-by-Step Details

## 1. Preprocessing the Data
Once the Kaggle set was downloaded, I did a quick check on the data to make sure each row had an ID and link to an image with Tableau Prep. I did not find any rows without these properties.
<br/>

Then, I downloaded all the images to my local machine and uploaded them to Google Cloud Platform storage. Because of the way I uploaded them, I had to fix the directories with [script.sh](https://github.com/skuretski/CourseProject/blobl/main/script.sh). This was a minor setback which took a couple hours to complete. 
<br/>

## 2. Performing Optical Character Recognition
Once the images were in storage, I wrote a Python script to perform OCR and translation [OcrProcessing.py](https://github.com/skuretski/CourseProject/blobl/main/OcrProcessing.py). I decided to do translation as well so that I could filter out non-English text. Out of the 3327 images, 3031 met the criteria of non-null English text. Some of the memes were just images with no text in them, or they had another language as their primary text. 

## 3. Cleaning Text Data
After doing OCR, it was important to do some regular expressions to clean up things like:
- contractions
- newlines and whitespace
- numbers
- non-alphabetical characters
- commonly found slang or misspellings e.g. shes -> she is or ur -> you are

## 4. Stop Words and Stemming
For stop words and stemming, I used Natural Language Toolkit (NLTK) for Python. I did add some additional stop words based on my findings with the memes, like "meme" and "rdankmemes" which was a Reddit tag. For stemming, I used a Porter stemmer since it is relatively fast and works well with the English language. The Porter stemmer is:

> "Based on the idea that the suffixes in the English language are made up of a combination of smaller and simpler suffixes." [1] (https://www.geeksforgeeks.org/introduction-to-stemming/)

## 5. TF-IDF Vectorization
Once stop words were 