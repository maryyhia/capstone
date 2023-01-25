
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

consumer_key = 'ipRSSBuXCVYFJaH4HUJ38hthX'
consumer_secret = 'WmHCmpY4XlCjXZgrXBw4tyKrj8Q9YrMFihjkujF7pj7gvubX5j'
access_token = "1611988991540359168-RLRq6cKrvGNnT4jJTWeACwldPYFMSW"
access_token_secret = "aoEy74xtYZDP2LCEe2tWCvgQpfBHZTRJAbIm10LpHyYxd"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAApclAEAAAAA7OC61TbdTEi7fRuU%2FUEqcxTltG0%3DWPxMXIOvjUChlVL8pODubf4dVw9GqUOPdeIH9p7CkykOH74700"
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








#  data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
#         data['Clean_Tweet'] = data['Tweets'].apply(clean_text)
#         pred = model.predict(data['Clean_Tweet'])
#         data['Sentiment'] = pred.tolist()
#         data['Date'] = np.array([tweet.created_at for tweet in tweets]).tolist()

#         # date_data = pd.DataFrame(data=[tweet.created_at for tweet in tweets], columns=['Date'])
#         # all_data = pd.concat([date_data, data], axis=1 )
#         st.write(data).head()


        # for tweet in tweets:
        #     tweet_list = [i.text for i in tweets]
        #     p = [i for i in classifier(tweet_list)]
        #     q=[p[i]['label'] for i in range(len(p))]
        #     df = pd.DataFrame(list(zip(tweet_list, q)),columns =['Latest Tweets on '+search_words, 'Sentiment'])
        #     st.write(df)



# include piechart to show general sentiments of the topic ranging 1year. 
# include scatter plot to show general sentiments of the topic ranging 1year. 



# def run():

#     with st.form(key='Enter topic'):
#         search_words = st.text_input('Enter topic')
#         number_of_tweets = st.number_input('Enter the number of latest tweets for which you want to know the sentiment(Maximum 50 tweets)', 0,50,10)
#         submit_button = st.form_submit_button(label='Submit')

#     if submit_button:
#         tweets =tw.Cursor(api.search_tweets, q = search_words, lang="en").items(number_of_tweets)
#         tweet_list = [i.text for i in tweets]
#         p = [i for i in classifier(tweet_list)]
#         q=[p[i]['label'] for i in range(len(p))]
#         df = pd.DataFrame(list(zip(tweet_list, q)),columns =['Latest '+str(number_of_tweets)+' Tweets'+' on '+search_words, 'Sentiment'])
#         st.write(df)	

# if __name__=='__main__':
#     run()


    # if submit_button:
    #     tweets =tw.Cursor(api.search_tweets, q = search_words,lang="en").items(number_of_tweets)
    #     tweet_list = [i.text for i in tweets]
    #     clean_tweet = list(map(clean_text, tweet_list))
    #     p = [i for i in model.predict(clean_tweet)]
    #     q=[p[i]['label'] for i in range(len(p))]
    #     df = pd.DataFrame(list(zip(tweet_list, q)),columns =['Latest '+str(number_of_tweets)+' Tweets'+' on '+search_words, 'Sentiment'])
    #     st.write(df)



        # client = tw.API(auth, wait_on_rate_limit=True)

        # def get_tweets(twitter_user_name, page_limit = 16, count_tweet=200):
        #     all_tweets = []
        #     for page in tw.Cursor(client.user_timeline, 
        #                 screen_name=twitter_user_name, 
        #                 count=count_tweet).pages(page_limit):
        #         for tweet in page:
        #             parsed_tweet = {}
        #             parsed_tweet['date'] = tweet.created_at
        #             parsed_tweet['text'] = tweet.text
                
        #         all_tweets.append(parsed_tweet)    
        #     # Create dataframe 
        #     df = pd.DataFrame(all_tweets)    
        #     # Revome duplicates if there are any
        #     df = df.drop_duplicates( "text" , keep='first')    
        #     return df  



        #         fig_col1, fig_col2 = st.columns(2)
        # with fig_col1:
        #     px.line(data, x=data['Date'], y=data['Sentiment'])
        #     st.plotly_chart(fig_col1)
        # with fig_col2:
        #     px.pie(values=data['Date'], names=data['Sentiment'])
        #     st.plotly_chart(fig_col2)
    