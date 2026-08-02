-- ============================================================
-- CFPB Consumer Complaints — BigQuery EDA Queries
-- Dataset: bigquery-public-data.cfpb_complaints.complaint_database
-- ============================================================

-- 1. Total complaint volume and date range
SELECT
  COUNT(*) AS total_complaints,
  MIN(date_received) AS earliest,
  MAX(date_received) AS latest
FROM
  `bigquery-public-data.cfpb_complaints.complaint_database`;

-- Result: 3,458,906 complaints, Dec 2011 – Mar 2023


-- 2. Complaint volume by product category
SELECT
  product,
  COUNT(*) AS complaint_count
FROM
  `bigquery-public-data.cfpb_complaints.complaint_database`
GROUP BY
  product
ORDER BY
  complaint_count DESC;

-- Result: Credit reporting dominates (~50% of all complaints)


-- 3. Company response breakdown
SELECT
  company_response_to_consumer,
  COUNT(*) AS complaint_count
FROM
  `bigquery-public-data.cfpb_complaints.complaint_database`
GROUP BY
  company_response_to_consumer
ORDER BY
  complaint_count DESC;

-- Result: "Closed with explanation" accounts for ~75% of responses


-- 4. Volume by state (top 15)
SELECT
  state,
  COUNT(*) AS complaint_count
FROM
  `bigquery-public-data.cfpb_complaints.complaint_database`
WHERE
  state IS NOT NULL
GROUP BY
  state
ORDER BY
  complaint_count DESC
LIMIT 15;

-- Result: CA, FL, TX lead (population-weighted)


-- 5. Yearly complaint volume trend
SELECT
  EXTRACT(YEAR FROM date_received) AS year,
  COUNT(*) AS complaint_count
FROM
  `bigquery-public-data.cfpb_complaints.complaint_database`
GROUP BY
  year
ORDER BY
  year;

-- Result: Steady year-over-year growth in complaint volume