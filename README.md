# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) Capstone Project: Tweet Sentiment & Toxic Tweets

------

## Background
Information and communication technology has chaged rapidly over the past 20 years, with a key development being the emergence of social media. The pace of change is accelerating. For example, the development of mobile technology has played an essential role in shaping the impact of social media. Mobile devices put the means to connect anywhere, at any time, on any device in everyone's hands. With the rise of social media, it brings about both positive and negative impact in the world we live.

In politics, the influence of social media in political campaigns has increased tremendously.It is known that most people receive their political news primarily through social media, and those who do get their news primarily through social media tend to be less well-informed and more likely to be exposed to unproven claims. 

The impact of social media on the society is bred through the internet. This is because social networks feed off interactions among people. Without social media, social, ethicial, environmental, and political ills would have minimal visibility. Increasaed visibility of issues has shifted the balance of power from the hands of a few to the masses. 

Businesses have realised they can use social media to generate insights, stimulate demand, and create targeted product offerings. These functions are important in the building blocks of businesses and in the world of e-commerce. The flipside would be the influence of social 'shares'. When products attract a lot of shares, it can reinforce sales. But when the reverse is true, customers begin to distrust the product and the company. 

In the world of work, social media has a profound effect on recruitment and hiring. Professional social networks like LinkedIn are important social mdia platforms for anyone looking to stand out in their profession. Employers and hiring managers make their decision based on information found on social media. 

Given the rise and effectiveness of social media, comes about a darker side to the coin. Cyberbullying have been noted and has risen over the years. The misuse of social media to spread rumours, share videos aimed at destroying reputations, and to blackmail others. Hateful comments can be seen on just about every platform including the gaming industry. Behind the shield of a screen, society have grown more confident in dishing toxic comments, of varying intensity, on social media as compared to face-to-face confrontation.  

It is clear that there needs to be a way of limiting the toxicity spreading over the internet. By being able to grasp the general sentiment a product, being an actual product, or a company's brand, or a person's image, it sways the general public's opinion. With this in mind, steps can be taken to reinforce positive returns. To add to this, by efficiently detecting toxic comments, and by their severity, it allows for it to be hidden or taken down. This not only reduces the negative impact its aimed to do, but to also reduce the corruption of hate in people's minds. 


------

## Problem Statement
#### Build a Sentiment analysis model with at least 90% accuracy toidentify between the different sentiments on Twitter tweets. Build a Toxic Comments multi-label model with at least 90% accuracy to rate the level of toxicity in comments on Twitter Tweets.

------

## Data sources
### Data used for model building
- [Twitter Sentiment Analysis](https://www.kaggle.com/datasets/jp797498e/twitter-entity-sentiment-analysis)
- [Toxic Comments Classification Challenge](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge)


### Twitter API v2
- Used to pull recent tweets for Streamlit app deployment
- Tweepy used for extraction

------

## Data Dictionary
### Sentiment Analysis Model
#### Dataset name: traindf 
##### This contains data from the kaggle source.
|Feature|Type|Description|
|---|---|---|
|Tweet_ID|int| ID of tweet|
|Topic|string| Topic the tweet is from|
|Sentiment|string|Sentiment of tweet|
|Tweet|string|Body of the tweet|
|Clean_Tweet|string|Tweets that have been processed and vectorized|


### Toxic Comments Model
#### Dataset name: traindf
##### This contains data from the kaggle source.
|Feature|Type|Description|
|---|---|---|
|comment_text|string| Body of comments|
|toxic|int| Binary of label|
|severe_toxic|int| Binary of label|
|obscene|int| Binary of label|
|threat|int| Binary of label|
|insult|int| Binary of label|
|identity_hate|int| Binary of label|
|clean_comments|string|Text that have been processed and vectorized|

------
### Streamlit App Deployment
![streamlit tweet](https://user-images.githubusercontent.com/115082902/214318625-317164f0-1bdd-48f0-98b0-3f68bc156272.jpg)
![streamlit viz](https://user-images.githubusercontent.com/115082902/214318646-d3a82b23-5e85-4fef-8ab6-2b486089ccd2.jpg)


------
### Key takeaways:
1. Best performing model for Sentiment Analysis Model used Count Vectorizer and Multinomial Naive Bayes with a accuracy score of 91%
2. Best performing model for Toxic Comments Model used TF-IDF and One vs Rest multi-label classifier with a accuracy score of 96%

------
### Limitations, Moving Forward, Conclusion
#### Limitations & Moving Forward
Sentiment Analysis Model
A larger dataset can be used to further train the model such as the Sentiment 140 dataset that has 1.6M rows of data. As many tweets contained abbreviations, training the model to identify and learn abbreivated words will increase model accuracy. Many tweets also included images/ gifs/ videos, a deep learning model can be used to read and analyse these. 

Toxic Comments Model
As the dataset only contained approximate 10% toxic- labelled data, more toxic-labeled data can be added to further increase model accuracy. Additionally, hyperparameter tuning of the models will also increase model accuracy and consistency. As the comments have varying lengths, and the dataset is fairly large, a deep learning model can be develop to identify and label toxic comemnts.

Twitter 
The API allows to search all recent tweets, but it does not have a language filter. This does not allow the model to train efficiently as it cannot filter for only English language tweets. By further developing the preproceses or by upgrading the Twitter API access, it may allow for either enabling the filter of only the English language, or by training across multiple languages. This is further increase model accuracy and consistency. 

Dashboard Development
With the Twitter API on hand, this allows for the creation of a real-time live dashboard showing incoming tweets in real-time and generating a moving graph plot to show the sentiments and also identify toxic comments. With this developed, it has uses in real-world such as in live events whereby gauging the performance of the event throught he sentiemnt analysis and byt detecting toxic comments and removing them before it spreads. 

#### Conclusion
Both models, Sentiment Analysis Model and Toxic Comments Model, achieved >90% accuracy. 91% for Sentiment Analysis Model, and 96% for Toxic Xomments Model. Further development of the models will allow for higher accuracy, consistency, and scalability. Accessibility to multiple languages nad mediums will allow the models to be train for efficient usage. And by creating a real-time live dashboard allows for various uses across industries. 

------
