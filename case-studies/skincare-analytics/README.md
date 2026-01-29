# Lead Optimization: Skincare Clinic Data Analysis

**Challenge:** Increase bookings without ad spend by identifying operational inefficiencies in lead management.

**Approach:** Analyzed lead submission data using Python and SQL to uncover friction points in the customer journey, then visualized findings via Looker Studio.

---

## 🔍 Key Insights

### 1. After-Hours Lead Leakage

**Discovery:** 13% of leads arrive at 9PM (after business hours)

**Impact:** 12+ hour response delay creates high churn risk

**Recommendation:** Implement automated lead capture for instant acknowledgment, reducing response time from next-day to immediate

---

### 2. Returning Customer Friction

**Discovery:** Returning customers show 25% drop-off rate vs. 100% conversion for new customers

**Impact:** Loyal customers frustrated by redundant form fields

**Recommendation:** Streamline booking flow for recognized users (pre-fill contact info, simplify form)

---

### 3. High-Value Service Targeting

**Discovery:** 30% of inquiries are for "Dark Spot/Melasma" treatments (via SQL analysis of service preferences)

**Impact:** Validates future paid media targeting strategy when budget becomes available

**Application:** Focus ad creative and messaging on pigmentation concerns rather than generic skincare

---

## 🛠️ Technical Workflow

### 1. Data Cleaning (Python)

**Challenge:** Raw lead data stored with nested JSON in CSV columns

**Solution:** Cleaned and structured data using pandas to parse JSON strings and map service IDs to readable names

**Code:** [View Python Script](./scripts/01_data_preprocessing.py)

---

### 2. Analysis (SQL)

**Challenge:** Enable scalable analysis if data volume grows

**Solution:** Wrote Standard SQL queries replicating the Python analysis, ready for BigQuery deployment

**Code:** [View SQL Queries](./queries/bigquery_analysis.sql)

**Key Queries:**

- Lead volume by hour of day
- Service preference distribution
- Conversion rate by customer type

---

### 3. Visualization (Looker Studio)

**Solution:** Connected processed data to Looker Studio dashboard

**Features:**

- Lead volume heatmap (by hour)
- Service demand breakdown
- Conversion funnel by customer type

![Dashboard Preview](./dashboard/dashboard_screenshot.png)

---

## 📊 Estimated Impact

**Projected Improvements (Pre-Implementation):**

- **13% lead capture gain** through 9PM automation
- **Reduced drop-off** for returning customers via UX optimization
- **Better ad targeting** when paid media budget becomes available

**Cost:** $0 (operational improvements only)

---

## 📂 Project Files

- `/data/` - Raw and processed CSV files
- `/queries/` - SQL analysis scripts
- `/reports/` - Strategy proposal and evidence
- `/docs/` - Data preprocessing methodology

---

## 🎯 Skills Demonstrated

- Data cleaning and transformation (Python/Pandas)
- SQL analysis (Standard SQL)
- Data visualization (Looker Studio)
- Conversion funnel optimization
- Business insight generation from raw data

---

_Client identity anonymized. All metrics represent actual analysis results._
