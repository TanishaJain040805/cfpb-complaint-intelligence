# Consumer Complaint Sentiment & Classification Pipeline (CFPB)

Analysis of 3.4M+ CFPB financial complaints: BigQuery EDA, a TF-IDF + Logistic
Regression classifier that routes complaint narratives to product categories,
VADER sentiment scoring, and an interactive dashboard (Power BI + Streamlit)
with **live model inference** - paste any complaint text and get a real-time
prediction.

This mirrors the "Customer Listening" workflow used in financial services
MIS teams - generating actionable insight from unstructured complaint text.

**Live app:** [cfpb-insights.streamlit.app](https://cfpb-insights.streamlit.app)

## Dataset

`bigquery-public-data.cfpb_complaints.complaint_database` - public BigQuery
dataset, 3,458,906 complaints (Dec 2011 - Mar 2023). A 50,000-row sample with
non-null narrative text was used for the ML portion.

## Methodology

1. **BigQuery EDA** (`queries.sql`) - volume by product/state/company response,
   yearly trend
2. **Text classification** - TF-IDF vectorization (10K features, unigrams +
   bigrams) + Logistic Regression (`class_weight='balanced'`), predicting
   product category from complaint narrative. 8 consolidated categories after
   merging duplicate/legacy labels and overlapping categories identified via
   confusion matrix analysis. Model and vectorizer are serialized
   (`tfidf_vectorizer.pkl`, `logreg_model.pkl`) and loaded directly into the
   Streamlit app for live inference.
3. **Sentiment analysis** - VADER compound scoring, aggregated by product,
   company, and time
4. **Dashboards** - Power BI (product volume, sentiment trend, top negative
   companies) + a Streamlit app (interactive state map, live metrics, and a
   live "try it yourself" prediction tool)

## Key Results

- **Classifier accuracy: 82.7%**, weighted F1: 0.83 (in line with published
  benchmarks of ~83-85% for this task)
- Dominant category (credit reporting) performs strongly (F1: 0.89); the
  weakest category, a merged "payday loan, title loan, or personal loan"
  group, improved from F1: 0.50 to **F1: 0.61** after merging it with the
  overlapping "vehicle loan" category - identified via confusion matrix
  analysis, since title loans are frequently secured against vehicles and
  share overlapping complaint language
- Sentiment splits nearly evenly negative/positive overall, but **debt
  collection complaints skew most negative** (-0.25 avg) while **student loan
  complaints skew most positive** (+0.10 avg)
- Clear sentiment dip starting 2020, consistent with pandemic-era financial
  stress
- Complaint volume is population-weighted (CA, FL, TX lead) and has grown
  steadily year over year since 2011

## Tech Stack

BigQuery (SQL) · Python (pandas, scikit-learn, VADER, Plotly, joblib) ·
Power BI (DAX) · Streamlit

## Limitations

- Classifier trained on a 50K-row sample, not the full complaint corpus
- Classification relies on product-specific language in the text - narratives
  with strong emotion but little product context (e.g. "this company is a
  scam") can be misclassified, since the model has no other signal to go on
- Sentiment scoring uses VADER (rule-based); doesn't capture nuanced or
  sarcastic language
- Rare product categories still have limited training data relative to
  dominant categories like credit reporting, which can affect model
  reliability for those classes despite the category merge improving results

## Files

- `cfpb_complaint_intelligence.ipynb` - full analysis notebook (EDA, model
  training, evaluation, confusion matrix)
- `queries.sql` - BigQuery EDA queries
- `app.py` - Streamlit dashboard with live model inference
- `requirements.txt` - Python dependencies
- `cfpb_complaints_for_powerbi.csv` - processed dataset used in Power BI/Streamlit
- `tfidf_vectorizer.pkl`, `logreg_model.pkl` - serialized model artifacts used
  by the live prediction feature
