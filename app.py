import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(page_title="CFPB Complaint Intelligence", layout="wide")
st.title("Consumer Complaint Sentiment & Classification Pipeline")
st.markdown("Analysis of CFPB financial complaints: product classification, sentiment scoring, and geographic trends.")

df = pd.read_csv("cfpb_complaints_for_powerbi.csv")

col1, col2, col3 = st.columns(3)
col1.metric("Total Complaints Analyzed", f"{len(df):,}")
col2.metric("Classifier Accuracy", "82.7%")
col3.metric("Negative Sentiment Share", f"{(df['sentiment_label']=='negative').mean()*100:.1f}%")

st.subheader("Complaint Volume by State")
state_counts = df.groupby('state').size().reset_index(name='complaint_count')
fig_map = px.choropleth(
    state_counts, locations='state', locationmode='USA-states',
    color='complaint_count', scope='usa', color_continuous_scale='Blues'
)
st.plotly_chart(fig_map, use_container_width=True)

st.subheader("Sentiment by Product Category")
sentiment_by_product = df.groupby('product_clean')['sentiment_score'].mean().sort_values()
st.bar_chart(sentiment_by_product)

st.subheader("Try it yourself")
st.markdown("Paste a complaint narrative below to see the model classify it and score its sentiment in real time.")

@st.cache_resource
def load_model():
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    clf = joblib.load("logreg_model.pkl")
    return vectorizer, clf

vectorizer, clf = load_model()
analyzer = SentimentIntensityAnalyzer()

user_text = st.text_area(
    "Complaint narrative:",
    placeholder="e.g. I have been trying to get my credit report corrected for three months and no one will respond..."
)

if user_text:
    X_input = vectorizer.transform([user_text])
    prediction = clf.predict(X_input)[0]

    sentiment_score = analyzer.polarity_scores(user_text)['compound']
    if sentiment_score >= 0.05:
        sentiment_label = "Positive"
    elif sentiment_score <= -0.05:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    pred_col1, pred_col2 = st.columns(2)
    pred_col1.metric("Predicted Product Category", prediction)
    pred_col2.metric("Sentiment", sentiment_label, f"{sentiment_score:.2f}")
