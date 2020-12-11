# CS410 Fall 2020 Course Project
Written by Susie Kuretski (skure2@illinois.edu)

# Topic
Utilizing Google Vision's optical character recognition to perform K-means cluster analysis

# Overview
From this [Kaggle](https://www.kaggle.com/sayangoswami/reddit-memes-dataset) dataset, which includes data for ~3300 Reddit memes, I extracted the image and uploaded it to Google Cloud Platform storage bucket. Then, I ran these images through optical character recognition and translation using Google Vision and Translate. Link to API docs [here](https://cloud.google.com/vision/docs/ocr). Once this was done, the results were stored in a GCP bucket as JSON data. An example would be:

[!85805u](./85805u.jpg?raw=true "85805u")

`{` <br />
`"src_lang": "en",`<br/>
`"text": "When you don't study for a test\nand get all the answers right\nSo this is the power of Ultra Instinct?\n",`<br/> 
`"file_name": "85805u.jpg",`<br/> 
`"id": "85805u"`<br/>
`}`
