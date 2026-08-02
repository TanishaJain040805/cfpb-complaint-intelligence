
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CFPB Complaint Intelligence", layout="wide")
st.title("Consumer Complaint Sentiment & Classification Pipeline")
st.markdown("Analysis of CFPB financial complaints: product classification, sentiment scoring, and geographic trends.")

df = pd.read_csv("cfpb_complaints_for_powerbi.csv")

col1, col2, col3 = st.columns(3)
col1.metric("Total Complaints Analyzed", f"{len(df):,}")
col2.metric("Classifier Accuracy", "81.8%")
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
