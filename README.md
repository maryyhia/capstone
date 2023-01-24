# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) Capstone Project: Tweet Sentiment & Toxic Tweets

------

## Background
There has been a surge in demand for data professionals in recent years. This led to an increased competition in the space for coding bootcamps. Competitors like Hack Reactor, Le Wagon, Vertical Institute, and Rocket Academy, have risen to meet the demands. If no action is taken, General Assembly may be faced with decline in market share, poor marketing ROI, and poorer lead generation. 

The General Assembly marketing team would need to better identify the online presence of a bootcamp seeker as opposed to that of the computer science major to aid in tergeted advertising. As both are fairly similar in nature, efforts to further segregate the two targets could yield better advertising ROI.

Keywords are an important aspect of the digital advertising, allowing for targeted strategies at all levels of the marketing funnel. They also guide marketing teams on the sort of advertising content that is required.

Thus, the aim is to segment and target the right audience for amrketing efforts streamline marketing efforts, rasie brand awareness with interested individuals, and increase advertising ROI. 

------

## Problem Statement
#### Build a model with at least 90% accuracy that helps to identify between those who are looking for bootcamp style learning as oppose to computer science majors or prospective students based on the words they use online.

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
![streamlit](relative/path/to/img.jpg?raw=true "Title")

------
### Key takeaways:
1. Best performing model used N-gram Count Vectorizer and Multinomial Naive Bayes with a F1 score of 95% accuracy
2. Most mentioned words for r/codingbootcamp revolved around attaining a job
3. Most mentioned words for r/csMajors revolved around attaining an internship
4. r/codingbootcamp has emphasis on schools that offer bootcamps

------
### Next Steps, Recommendations, Conclusion
#### Moving forward
With more time and resources, more data could be gathered not just from reddit, but across various online platforms. This could help the model identify across mediums as well. Like videos, images, and short texts.

Along with that, a better understanding of the different acronyms and abbreviations within the text post would allow for a more thorough analysis and breakdown. 

Doing a sentiment analsis would also give a better picture of the difference between coding bootcamps and computer science majors. This allows for a different perspective of the students invovled in both educational choices. 

#### Recommendations
Using the model to look at keywords.
The features produced by the model will allow General Assembly marketing team to better identify suitable posts to engage with. 

Automating the model.
Deployment of the model to automatically scan the social media interations across platforms. This helps the team to collate just the posts they need to engage with and evaluate. 

Marketing efforts.
Boost marketing across channels to increase visibility and presence against competitors. By making use of the keywords marketing materials could hone in on those interested in the bootcamp type courses and maybe sway those looking at full degree programs to hop over. 

#### Conclusion
General Assembly needs to stand out from our competitors and be able to accurately and effectively identify potential students. There is a need to increase visibility and be quick in response. In today's fast paced environment, speed is also essential in being able to act before our competitors. 

The model is able to correctly identify around 95% of the users who are interested in coding bootcamps. This would allow General Assembly to better maximise the marketing outreach and increase our conversation rate. 

------
