import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title('Sentiment Analysis of Tweets of US Airlines')
st.sidebar.title('Sentiment Analysis of Tweets of US Airlines')

st.markdown(" This application is a Streamlit dashboard used to analyze the sentiment of Tweets 🐦")
st.sidebar.markdown(" This application is a Streamlit dashboard used to analyze the sentiment of Tweets 🐦")


DATA_URL = "Tweets.csv"
@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data = load_data()

st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio('Sentiment', ('positive', 'neutral', 'negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[['text']].sample(n=1).iat[0,0])

st.sidebar.markdown('### Number of tweets by sentiment')
select = st.sidebar.selectbox('Visualization type', ['Bar chart', 'Pie chart'], key = '1')
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

if not st.sidebar.checkbox('Hide', True):
    st.markdown('### Number of tweets by sentiment')
    if select == 'Bar chart':
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height = 500)
        st.plotly_chart(fig)
    elif select == 'Pie chart':
        fig = px.pie(sentiment_count, names='Sentiment', values='Tweets', color='Tweets', height = 500)
        st.plotly_chart(fig)

st.sidebar.subheader('Where and when are users tweeting from?')
hour = st.sidebar.slider('Hour of day', 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]
if not st.sidebar.checkbox('Close', True, key = '2'):
    st.markdown('### Tweets Locations bases on the time of day')
    st.markdown(f"{len(modified_data)} tweets between {hour}:00 and {(hour+1)%24}:00")
    st.map(modified_data)
    if st.sidebar.checkbox('Show raw data', False):
        st.write(modified_data)


st.sidebar.subheader('Breakdown airline tweets by sentiment')
choice = st.sidebar.multiselect('Pick the airline', (sorted(data['airline'].unique())), key = '3')

if len(choice) > 0:
    choice_data = data[data['airline'].isin(choice)]

    fig_choice = px.histogram(choice_data, x='airline', y = 'airline_sentiment',
    histfunc='count', color='airline_sentiment', facet_col='airline_sentiment',
    labels={'airline_sentiment': 'tweets'}, height=600, width=800)
    st.plotly_chart(fig_choice)

st.sidebar.subheader('Word Cloud')
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?',
('positive', 'neutral', 'negative'))

if not st.sidebar.checkbox('Close', True, key='4'):
    st.header(f'Word Cloud for "{word_sentiment}"')
    df = data[data['airline_sentiment']== word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)
    fig_word_cloud, ax = plt.subplots()
    ax.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot(fig_word_cloud)
