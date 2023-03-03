
import streamlit as st
import tweepy as tw
import pandas as pd
import numpy as np
import plotly.express as px
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from datetime import date

nltk.download('stopwords')
stopwords = set(stopwords.words('english'))

wn = WordNetLemmatizer()

# load model
model = pickle.load(open('model.pkl', 'rb'))
toxicmodel = pickle.load(open('toxic_model.pkl','rb'))
severetoxicmodel = pickle.load(open('severe_toxic_model.pkl','rb'))
obscenemodel = pickle.load(open('obscene_model.pkl','rb'))
threatmodel = pickle.load(open('threat_model.pkl','rb'))
insultmodel = pickle.load(open('insult_model.pkl','rb'))
identityhatemodel = pickle.load(open('identity_hate_model.pkl','rb'))

#load vectorizer
vectorizer = pickle.load(open('toxicvect2.pkl','rb'))

consumer_key = 'consumer key'
consumer_secret = 'consumer secret'
access_token = "access token"
access_token_secret = "access token secret"
bearer_token = "bearer token"
client = tw.Client(bearer_token)
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# st.set_page_config(layout="wide")

# make a dictionary of contractions
contractions = {"ain't": "is not", "aren't": "are not","can't": "cannot", "'cause": "because", "could've": "could have", "couldn't": "could not",
                           "didn't": "did not",  "doesn't": "does not", "don't": "do not", "hadn't": "had not", "hasn't": "has not", "haven't": "have not",
                           "he'd": "he would","he'll": "he will", "he's": "he is", "how'd": "how did", "how'd'y": "how do you", "how'll": "how will", "how's": "how is",
                           "I'd": "I would", "I'd've": "I would have", "I'll": "I will", "I'll've": "I will have","I'm": "I am", "I've": "I have", "i'd": "i would",
                           "i'd've": "i would have", "i'll": "i will",  "i'll've": "i will have","i'm": "i am", "i've": "i have", "isn't": "is not", "it'd": "it would",
                           "it'd've": "it would have", "it'll": "it will", "it'll've": "it will have","it's": "it is", "let's": "let us", "ma'am": "madam",
                           "mayn't": "may not", "might've": "might have","mightn't": "might not","mightn't've": "might not have", "must've": "must have",
                           "mustn't": "must not", "mustn't've": "must not have", "needn't": "need not", "needn't've": "need not have","o'clock": "of the clock",
                           "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not", "sha'n't": "shall not", "shan't've": "shall not have",
                           "she'd": "she would", "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have", "she's": "she is",
                           "should've": "should have", "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have","so's": "so as",
                           "this's": "this is","that'd": "that would", "that'd've": "that would have", "that's": "that is", "there'd": "there would",
                           "there'd've": "there would have", "there's": "there is", "here's": "here is","they'd": "they would", "they'd've": "they would have",
                           "they'll": "they will", "they'll've": "they will have", "they're": "they are", "they've": "they have", "to've": "to have",
                           "wasn't": "was not", "we'd": "we would", "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", "we're": "we are",
                           "we've": "we have", "weren't": "were not", "what'll": "what will", "what'll've": "what will have", "what're": "what are",
                           "what's": "what is", "what've": "what have", "when's": "when is", "when've": "when have", "where'd": "where did", "where's": "where is",
                           "where've": "where have", "who'll": "who will", "who'll've": "who will have", "who's": "who is", "who've": "who have",
                           "why's": "why is", "why've": "why have", "will've": "will have", "won't": "will not", "won't've": "will not have",
                           "would've": "would have", "wouldn't": "would not", "wouldn't've": "would not have", "y'all": "you all",
                           "y'all'd": "you all would","y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have",
                           "you'd": "you would", "you'd've": "you would have", "you'll": "you will", "you'll've": "you will have",
                           "you're": "you are", "you've": "you have"}

def clean_text(text):
    # convert to lower case
    text = text.lower()
    #remove user handle
    text = re.sub("@[\w]*", '', text)
    #remove http links
    text = re.sub("http\S+", '', text)
    #remove digits and spl characters
    text = re.sub("[^a-zA-Z#]", ' ', text)
    #remove contractions
    text = ' '.join([contractions[t] if t in contractions else t for t in text.split(" ")])
    #tokenize text
    tokens = re.split('\W+', text)
    #remove stopwords
    text = ' '.join([wn.lemmatize(word) for word in tokens if word not in stopwords])
    # remove hashtag
    text = re.sub('(#[A-Za-z]+[A-Za-z0-9-_]+)', '', text)
    #remove rt characters
    text = re.sub("rt", '', text)
    #remove additional spaces
    text = re.sub("\s+", ' ', text)
    
    return text

START = '2023-01-01'
TODAY = date.today().strftime('%Y-%m-%d')

with st.container():
    st.title('Tweets Sentiment')
    st.markdown('This app uses tweepy to get tweets from twitter based on the input topic. It then processes the tweets through self-trained model for sentiment analysis and toxic comment classification.')


with st.container():
    search_words = st.text_input('Enter topic')
    submit_button = st.button('Submit')

    if submit_button:
        tweets = tw.Paginator(client.search_recent_tweets, query=search_words,
                              tweet_fields=['context_annotations', 'created_at'], max_results=100).flatten(limit=1000)
        
       # create a list of records
        tweet_info_ls = []
        # iterate over each tweet and corresponding user details
        for tweet in tweets:
            tweet_info = {
                'Date': tweet.created_at,
                'Tweets': tweet.text,
            }
            tweet_info_ls.append(tweet_info)
        # create dataframe from the extracted records
        data = pd.DataFrame(tweet_info_ls)

        data['Clean_Tweet'] = data['Tweets'].apply(clean_text)
        pred = model.predict(data['Clean_Tweet'])
        data['Sentiment'] = pred.tolist()

        data_display = data[['Tweets', 'Sentiment']]

        st.write(data_display)

        # Visualisation
        colors = ['crimson', 'darkblue', 'darkcyan','darkorange']
        fig1 = px.histogram(data, x=data['Sentiment'])
        st.plotly_chart(fig1)

        fig2 = px.pie(data, names=data['Sentiment'])
        st.plotly_chart(fig2)

        # Toxic comment classification
        categories = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']

        topred = vectorizer.transform(data['Clean_Tweet'])
        toxicpred1 = toxicmodel.predict(topred)
        data[categories] = toxicpred1.tolist()

        toxicpred2 = severetoxicmodel.predict(topred)
        data[categories] = toxicpred2.tolist()

        toxicpred3 = obscenemodel.predict(topred)
        data[categories] = toxicpred3.tolist()

        toxicpred4 = threatmodel.predict(topred)
        data[categories] = toxicpred4.tolist()

        toxicpred5 = insultmodel.predict(topred)
        data[categories] = toxicpred5.tolist()

        toxicpred6 = identityhatemodel.predict(topred)
        data[categories] = toxicpred6.tolist()


        data_display2 = data['Tweets',categories]

        st.write(data_display2)







