# Project Media Insights
Developed by Darren Colby and Jessup Jong

Get insights into your user inteaction on YouTube. This tool enables you to
quickly see trends in comments and sentiments in your videos. We produce time series 
predictions by day, month, year, and autoregression components using a Bayesian Markov Chain Monte Carlo Prophet, a time series library developed by Facebook. 
Sentiment classification is based on VADER using preprocessed text. 
When conducting sentiment classification, the program 
removes emojis, newlines, tabs, carriage returns, punctuation, and numbers before
translating any foreign text to English and correcting misspelled words. This 
program allows you to visualize the similarity of competitor videos by using
the cosine similarity of the GloVe embeddings of their transcripts. Finally,
you can use the upload module to automate video uploads.

## Features

* Automate video uploads
* Can be run by double clicking a bash file
* Automatic translation of comments and transcripts to English
* Automatic spelling correction
* Cosine similarities calculated based on GloVe embeddings
* Change the forecast period with a slider
* Uploads secured by OAuth

## Data Sources
* comment data directly from YouTube using GET requests
* youtube_transcript_api third party library for video transcripts
* gensim for pretrained GloVe model weights and tokens

## Usage
### Using the automate.sh script
```Python
cd media_insights
automate.sh
```
Alternatively run by double clicking on automate.sh

### Makefile
```Shell
cd media_insights
make
```

## Demo Version
In addition to running the program locally, you can interact with a live version at https://mediainsights.streamlit.app
