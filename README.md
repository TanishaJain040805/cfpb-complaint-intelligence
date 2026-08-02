# Consumer Complaint Sentiment & Classification Pipeline (CFPB)

Analysis of 3.4M+ CFPB financial complaints: BigQuery EDA, a TF-IDF + Logistic
Regression classifier that routes complaint narratives to product categories,
VADER sentiment scoring, and an interactive dashboard (Power BI + Streamlit).

This mirrors the "Customer Listening" workflow used in financial services
MIS teams - generating actionable insight from unstructured complaint text.

## Dataset

`bigquery-public-data.cfpb_complaints.complaint_database` - public BigQuery
dataset, 3,458,906 complaints (Dec 2011 – Mar 2023). A 50,000-row sample with
non-null narrative text was used for the ML portion.

## Methodology

1. **BigQuery EDA** (`queries.sql`) - volume by product/state/company response,
   yearly trend
2. **Text classification** - TF-IDF vectorization (10K features, unigrams +
   bigrams) + Logistic Regression, predicting product category from complaint
   narrative. 9 consolidated categories after merging duplicate/legacy labels.
3. **Sentiment analysis** - VADER compound scoring, aggregated by product,
   company, and time
4. **Dashboards** - Power BI (product volume, sentiment trend, top negative
   companies) + a Streamlit app (interactive state map, live metrics)

## Key Results

- **Classifier accuracy: 81.8%**, weighted F1: 0.82 (in line with published
  benchmarks of ~83-85% for this task)
- Dominant category (credit reporting) performs strongly (F1: 0.89); rarer
  categories like vehicle loans are weaker (F1: 0.50) due to data scarcity -
  noted honestly rather than hidden
- Sentiment splits nearly evenly negative/positive overall, but **debt
  collection complaints skew most negative** (-0.25 avg) while **student loan
  complaints skew most positive** (+0.10 avg)
- Clear sentiment dip starting 2020, consistent with pandemic-era financial
  stress
- Complaint volume is population-weighted (CA, FL, TX lead) and has grown
  steadily year over year since 2011

## Tech Stack

BigQuery (SQL) · Python (pandas, scikit-learn, VADER, Plotly) · Power BI (DAX)
·
