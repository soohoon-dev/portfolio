/*
 * Project: Skincare Clinic Lead Optimization
 * Tech Stack: Google BigQuery (Standard SQL)
 * Context: 
 * This script runs analytics on the pre-processed lead data (`cleaned_leads`).
 * The raw JSON logㄴs were transformed via Python (Pandas) ETL pipeline 
 * before being loaded into the Data Warehouse to ensure schema consistency.
 */

-- =========================================================
-- 1. Analysis: The "9 PM Golden Time" Discovery
-- =========================================================
-- Objective: Identify lead volume by hour to justify the 'Night-Shift Automation' proposal.
-- Insight: A significant volume of leads arrives after business hours (21:00).

SELECT
  hour AS hour_of_day,
  COUNT(Id) AS total_leads,
  
  -- Calculate potential revenue lost (Assumption: $200 avg. LTV per lead)
  COUNT(Id) * 200 AS estimated_opportunity_value,
  
  -- Categorize into Operational Status (Business Hours: 9 AM - 6 PM)
  CASE 
    WHEN hour BETWEEN 9 AND 18 THEN 'Business Hours'
    ELSE 'Off-Hours (Risk of Churn)'
  END AS operational_status
FROM
  `skincare_optimization.cleaned_leads`
GROUP BY
  hour
ORDER BY
  total_leads DESC;


-- =========================================================
-- 2. Analysis: Service Demand for Targeting
-- =========================================================
-- Objective: Identify the top requested services among New Customers to optimize Ad Targeting.
-- Insight: "Dark Spot / Melasma" is the #1 organic driver for new acquisition.

SELECT
  service_name,
  COUNT(Id) AS request_count,
  
  -- Calculate percentage share of total requests
  ROUND(
    COUNT(Id) * 100.0 / SUM(COUNT(Id)) OVER(), 
    1
  ) AS percentage_share
FROM
  `skincare_optimization.cleaned_leads`
WHERE
  customer_type = 'New' -- Filter: Focus strictly on New Acquisition
GROUP BY
  service_name
ORDER BY
  request_count DESC;


-- =========================================================
-- 3. Analysis: Funnel Friction (New vs. Returning)
-- =========================================================
-- Objective: Compare completion rates to validate the need for a simplified Returning User form.
-- Insight: Returning users show higher churn due to redundant form fields.

SELECT
  customer_type,
  COUNT(Id) AS total_attempts,
  SUM(is_complete) AS successful_bookings,
  
  -- Calculate Conversion Rate
  ROUND(
    SUM(is_complete) * 100.0 / COUNT(Id), 
    1
  ) AS conversion_rate_percent
FROM
  `skincare_optimization.cleaned_leads`
GROUP BY
  customer_type
ORDER BY
  conversion_rate_percent DESC;