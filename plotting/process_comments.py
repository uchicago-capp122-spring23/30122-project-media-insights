"""
Author: Darren Colby
"""

import re
import json
import translators
import pandas as pd
import spacy
from autocorrect import Speller
from time import sleep
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from spacy.lang.en.stop_words import STOP_WORDS

# This should also be a stopword
STOP_WORDS.add('s')

# Credit: https://stackoverflow.com/questions/51217909/removing-all-emojis-from-text
EMOJI_PATTERN = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF" 
        u"\U0001F680-\U0001F6FF" 
        u"\U0001F1E0-\U0001F1FF" 
        u"\U0001F1F2-\U0001F1F4" 
        u"\U0001F1E6-\U0001F1FF" 
        u"\U0001F600-\U0001F64F"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U0001F1F2"
        u"\U0001F1F4"
        u"\U0001F620"
        u"\u200d"
        u"\u2640-\u2642"
        "]+", flags=re.UNICODE)

# Downloads the lemmas and stopwords if they don't exist
try:
    en_model = spacy.load('en_core_web_lg', disable = ['parser','ner'])
except:
    spacy.cli.download("en_core_web_lg")
    en_model = spacy.load('en_core_web_lg', disable = ['parser','ner'])


def remove_emojis(text: str):
    """
    Remove emojis from strings

    Parameters:
        text (str): The input string

    Returns:
        (str) The string with emojis removed
    """
    cleaner_text = EMOJI_PATTERN.sub(r'', text)

    return cleaner_text


def preprocess_comments(raw_comments: pd.Series, fast: bool=False):
    """
    Preprocess comments by removing emojis, newline, tab, and carriage return characters; 
    removing punctuation and extra spaces; converting to lowercase; spell checking; and 
    translating them to English

    Parameters:
        raw_comments (pd.Series): Raw comments to preprocess
        fast (bool): If this is set to False, translation to English is performed

    Returns:
        (pd.DataFrame) A dataframe with text and date columns for a given video
    """
    clean_comments, clean_dates = [], []
    corrector = Speller()

    for comm_lst in raw_comments:
        for comm in comm_lst:
            text, date = comm[0], comm[1]
            no_emojis = remove_emojis(text)
            no_newline = re.sub(r'[\r\n\t]', '', no_emojis)
            no_punct = re.sub(r'[^\w\s]', '', no_newline)
            no_extra_space = re.sub(r'\s+', ' ', no_punct)
            lowercase = no_extra_space.strip().lower()
            no_links = re.sub(r'http\S+', '', lowercase)

            if fast:
                # Spell checking
                better_spelling = corrector(no_links)
            else:
                # Translate to english
                sleep(1)
                translation = translators.translate_text(no_links)

                better_spelling = corrector(translation)

            # Lemmatize and remove stopwords
            doc = en_model(better_spelling)
            clean_doc = " ".join([tok.lemma_ for tok in doc 
                                  if tok.lemma_ not in STOP_WORDS and len(tok.lemm_) < 2])

            clean_comments.append(clean_doc); clean_dates.append(date)

    return pd.DataFrame(zip(clean_comments, clean_dates), columns=['text', 'date'])


def calculate_comment_sentiment(text: str):
   return SentimentIntensityAnalyzer().polarity_scores(text)['compound']


if __name__ == '__main__':
    with open("../data/cleaned_comment_data.json",'r') as f:
        data = json.loads(f.read())

    raw_comments = pd.json_normalize(data)

    clean_text = preprocess_comments(raw_comments.iloc[:, 0])
    clean_text['sentiment'] = clean_text.apply(lambda r: calculate_comment_sentiment(r.text), 
                                           axis=1)
    clean_text.to_csv("../data/preprocessed_comments.csv")

