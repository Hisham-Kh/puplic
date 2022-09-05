import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud , STOPWORDS
from PIL import Image



def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://c.tenor.com/ZEX0M35v0Y4AAAAi/frames-frame.gif");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

st.markdown("<h1 style='text-align: center; color: grey;'>Sentiments Analaysis of Tweets about US Airlines</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: green; font-size : 13px'> 👉 👉 If the sidebar is not shown..click the arrow at the upper left corner</h1>", unsafe_allow_html=True)



col1, col2, col3 = st.columns(3)
with col2:
    st.image('https://thumbs.gfycat.com/SecondInconsequentialBasil-size_restricted.gif',  width =350)




st.sidebar.markdown("<h1 style='text-align: center; color: white; background-color: lightblue ;'> Sentiments Analaysis of Tweets about US Airlines </h1>", unsafe_allow_html=True)
st.sidebar.markdown("<h1 style='text-align: center; color: blue;  font-size: 15px '> made by Hisham.K</h1>", unsafe_allow_html=True)

data_url =("https://github.com/Hisham-Kh/puplic/raw/puplic/Tweets.csv")
@st.cache(persist=True)


def load_data():
    data=pd.read_csv(data_url)
    data['tweet_created']=pd.to_datetime(data['tweet_created'])
    return data
data = load_data()
st.sidebar.subheader("Random Tweets")

if  st.sidebar.checkbox("Show / Hide a random tweet" , False, key ='6'):

    random_tweet = st.sidebar.radio("Choose the type of tweet",('positive', 'neutral', 'negative'), horizontal = True)
    st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])
st.sidebar.subheader("Number of Tweets by Sentimnt")
V=st.sidebar.selectbox('Choose Visualization Type', ['Histogram','Pie Chart'], key ='1' )
tcounts = data['airline_sentiment'].value_counts()
if not st.sidebar.checkbox("Hide Visualization",True):
    st.markdown("### Number of Tweets by Sentimnt")
    if V == 'Histogram':
        fig=px.histogram(tcounts,x = tcounts.index,y =tcounts.values , color = tcounts.values)
        st.plotly_chart(fig)
    if V == 'Pie Chart':
        fig=px.pie(tcounts,values=tcounts.values, names =tcounts.index )
        st.plotly_chart(fig)
else:
    st.markdown("<h1 style='text-align: center; color: black ; font-size :20px'> This data originally came from Crowdflower's Data for Everyone library. Twitter data was scraped from February of 2015 and contributors were asked to first classify positive, negative, and neutral tweets, followed by categorizing negative reasons (such as late flight or rude service) The data we are providing on Kaggle is a slightly reformatted version of the original source  It includes both a CSV file and SQLite database </h1>", unsafe_allow_html=True)

st.sidebar.subheader("When and Where Tweets Came from?")
hour = st.sidebar.slider("Hour of Day", 0 , 23)


mdata = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox('close map', True, key='2'):
    st.markdown('### Location of Tweets based on Time 24')
    st.markdown('%i tweets between %i:00 and %i:00' %(len(mdata), hour , (hour+1)%24))
    st.map(mdata)
    if st.sidebar.checkbox('Show raw data', False):
        st.write(mdata)
st.sidebar.subheader('Tweets based on Airline Company')
choice= st.sidebar.multiselect('choose Airline',('US Airways','United','American','Southwest','Delta','Virgin America' ), key ='3')
if len(choice)> 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice=px.histogram(choice_data, x= 'airline' , y ='airline_sentiment', histfunc = 'count', color = 'airline_sentiment' , facet_col = 'airline_sentiment',
    labels = {'airline_sentiment':'Tweets'} , height = 600 , width = 800)
    st.plotly_chart(fig_choice)
st.sidebar.subheader("Word Cloud")
word_s= st.sidebar.radio('Display word cloud for : ',('positive' , 'neutral', 'negative'), horizontal = True)
if not st.sidebar.checkbox("Hide word cloud", True , key = '7'):
    df= data[data['airline_sentiment']== word_s]
    words=''.join(df['text'])
    processed_words=''.join([word for word in words.split() if 'http' not in word and not word.startswith('@')])
    wordcloud = WordCloud(stopwords = STOPWORDS,background_color ='white' , height =640 , width = 800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()
st.set_option('deprecation.showPyplotGlobalUse', False)
