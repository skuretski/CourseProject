# CS410 Fall 2020 Course Project
Written by Susie Kuretski (skure2@illinois.edu)

# Topic
Utilizing Google Vision's optical character recognition to perform K-means cluster analysis on Reddit memes

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

__For steps 3-7, I used code from (Kaggle - Use DFoly1) [https://www.kaggle.com/dfoly1/k-means-clustering-from-scratch]__

## 1. Preprocessing the Data
Once the Kaggle set was downloaded, I did a quick check on the data to make sure each row had an ID and link to an image with Tableau Prep. I did not find any rows without these properties.
<br/>

Then, I downloaded all the images to my local machine and uploaded them to Google Cloud Platform storage. Because of the way I uploaded them, I had to fix the directories with [script.sh](https://github.com/skuretski/CourseProject/blob/main/script.sh). This was a minor setback which took a couple hours to complete. 
<br/>

## 2. Performing Optical Character Recognition
Once the images were in storage, I wrote a Python script to perform OCR and translation -- [OcrProcessing.py](https://github.com/skuretski/CourseProject/blob/main/OcrProcessing.py). I decided to do translation as well so that I could filter out non-English text. Out of the 3327 images, 3031 met the criteria of non-null English text. Some of the memes were just images with no text in them, or they had another language as their primary text. 

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
Once stop words and stemming was done, I transformed the text from the memes into a TF-IDF vector using `sklearn`. This method has many options like n-gram range, maximum or minimum document frequency, maximum features, smoothing, and using sublinear term frequency. I tried different variations of TF-IDF vectorization to see how that would affect K-means clustering. With this specific dataset, the maximum number of features seemed to be optimal around 1000-1500. Anything beyond this would cause the clustering to have a lot of outliers, resulting in imbalanced and poorly grouped clusters. I also tried the sublinear term frequency option, but that caused some irregularities as well, similar to increasing number of features. 

## 6. Principal Component Analysis 
Before doing K-means, I did do PCA to reduce dimensionality in the TF-IDF vector. If we look at the TF-IDF vector, the X axis is the meme text and the Y axis is one of the 1500 features or terms. Where [X,Y] meet is the term frequency. With 1500 features and 3031 meme text data segments, it's useful to construct a new feature subspace to reduce the risk of overfitting because the data is too generalized.

## 7. K-means
K-means is an algorithm very similar to EM algorithm where there is an assignment-like phase and then a maximize phase. In K-means, we first initialize cluster centroids randomly. Then, repeat this until convergence: 
- For every data point, assign to nearest centroid via Euclidean distance
- Move the centroids to the center of data points assigned to it
<br/>


For K-means clustering, I did do multiple runs with 2-6 clusters. I set maximum iterations to 600, but generally, it converged in < 100 iterations. With `sklearn`, it can do multiple randomized initializations in order to find the best possible local maxima, which may or may not be the global maxima. The default is 10, but I tried different ranges which usually didn't have much variance.

## 8. What is a good number of clusters?
I used 2 methods in determining what might a good number of clusters look like:
1. Elbow method
2. Silhouette analysis

The Elbow method is a heuristic approach in which the number of clusters is plotted against the function of variance. A "good" number is where the curve has a definitive bend, resembling the shape of a human arm with an elbow. Generally, 3 clusters provided the best elbow. However, with some different variations of the TF-IDF vector and K-means, the bend was not explicit and was actually a smooth curve, which is one of the drawbacks of using the Elbow method.

The Silhouette analysis measures the separation distance between clusters. The range of silhouette analysis can range from -1 to 1. 
- A value of 1 suggests the sample is far away from neighboring clusters.
- A value of zero suggests the sample is very close to the boundary between two clusters.
- A negative value suggests the sample may have been assigned to the wrong cluster.

My results usually had values of > 0.75 for `n` clusters of 2-3, while it dropped off to < 0.5 for > 5 clusters. I did not observe any negative or zero values. 

I used code from [scikit learn](https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html#sphx-glr-auto-examples-cluster-plot-kmeans-silhouette-analysis-py) to do my silhouette analysis. 
<br/>

With the Elbow method and silhouette analysis, it seemed that 3 was a good number of clusters for this data. 

## 9. Results
Overall, 3 clusters seemed to be the magic number based on evaluation. Selecting features > 1500 seemed to be detrimental to clustering where the clusters were very skewed and had many outliers, even with PCA dimensionality reduction. 

The 3 clusters had these top words:
1. `will`, `people`, `now`, `see`, `man`, `know`, `time`
2. `win`, `boi`, `years`, `body`, `entire`, `million`, `master`
3. `pm`, `likes` `retweets`, `trump`, `follow`, `donald`, `will`

While some themes were not extremely clear like in cluster 1 and cluster 2, the third cluster was quite clear in terms of having a social media vibe. Other top words in this third cluster were `realdonaldtrump`, `elonmusk`, and `replying`. 

For improvements, it might be useful to try different stemming methods and adding more stopwords like "will" or "us." But here is where ambiguity comes into play. Without looking at each meme individually, it's hard to tell if will was in the context of an auxillary verb like "will travel," or a noun like a legal document. The same goes for "us." Does this mean us, like the group of us, or US like the United States? 

It would also be interesting to see bi-grams of this. When I did the TF-IDF vectorization, I stuck with unigrams since I just wanted to use bag of words representation before getting ahead of myself.

Overall, this project has been a great learning experience in terms of working with real data, using Google Vision, seeing how K-means works especially after doing EM algorithm work, and evaluation of clusters. 


