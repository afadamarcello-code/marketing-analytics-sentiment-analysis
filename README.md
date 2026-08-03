# 📈 Marketing Analytics & Customer Sentiment Analysis

## 📌 Project Overview
This project models an enterprise-level Marketing Analytics pipeline. It transforms raw, fragmented customer, product, and campaign data into structured database views, performs Natural Language Processing (NLP) sentiment analysis on customer reviews via Python, and models data into an interactive executive dashboard.

The goal is to analyze marketing efficiency, customer journey bottlenecks, and product feedback to deliver actionable, ROI-focused business strategies.

---

## 🗂️ Project Repository Structure

```text
marketing-analytics-sentiment-analysis/
│
├── data/                             # Raw & processed datasets
│   ├── raw_customers.csv
│   ├── raw_customer_journey.csv
│   ├── raw_customer_reviews.csv
│   ├── raw_engagement_data.csv
│   ├── raw_geography.csv
│   ├── raw_products.csv
│   └── fact_customer_reviews_with_sentiment.csv  # Output from Python NLP
│
├── sql_scripts/                      # T-SQL Cleaning & View Creation
│   ├── 01_clean_customers.sql
│   ├── 02_clean_products.sql
│   ├── 03_clean_customer_reviews.sql
│   ├── 04_clean_customer_journey.sql
│   └── 05_clean_engagement_data.sql
│
├── python/                           # Python ETL & Sentiment Pipeline
│   └── 06_sentiment_analysis.py
│
└── README.md                         # Documentation & Project Guide
```

---

## 🛠️ Database Setup & Restoration

This project relies on a Microsoft SQL Server database. If you wish to restore the full relational database locally from a `.bak` file:

1. Download the database backup file (`PortfolioProject_MarketingAnalytics.bak`) from [Google Drive / OneDrive Link Here].
2. Place the file in your SQL Server backup directory (e.g., `C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\Backup\`).
3. Execute the following T-SQL script in SQL Server / VS Code to restore the database:

```sql
-- Restore Database from Backup File
RESTORE DATABASE PortfolioProject_MarketingAnalytics
FROM DISK = 'C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\Backup\PortfolioProject_MarketingAnalytics.bak'
WITH REPLACE,
MOVE 'PortfolioProject_MarketingAnalytics' TO 'C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\PortfolioProject_MarketingAnalytics.mdf',
MOVE 'PortfolioProject_MarketingAnalytics_log' TO 'C:\Program Files\Microsoft SQL Server\MSSQL16.SQLEXPRESS\MSSQL\DATA\PortfolioProject_MarketingAnalytics_log.ldf';
```

---

## 🧹 Phase 1: SQL Data Cleaning & Transformation Layer

To ensure efficient staging and downstream analysis, raw database tables were cleaned and converted into modular database views (`dbo.vw_*`).

### Key SQL Logic Implemented:
* **`dbo.vw_dim_customers`**: Joined `dbo.customers` with `dbo.geography` to add spatial context to customer profiles.
* **`dbo.vw_dim_products`**: Cleaned and formatted product dimensions and pricing tiers.
* **`dbo.vw_fact_customer_reviews`**: Staged review text data for downstream Python Natural Language Processing (NLP).
* **`dbo.vw_fact_customer_journey`**: 
  * Implemented `ROW_NUMBER() OVER(PARTITION BY ...)` to identify and remove duplicate journey records.
  * Used `COALESCE()` combined with window functions (`AVG(Duration) OVER(PARTITION BY VisitDate)`) to impute missing visit durations.
* **`dbo.vw_fact_engagement_data`**: 
  * Cleaned inconsistent string values (e.g., `SocialMedia` $\rightarrow$ `Social Media`).
  * Used string manipulation (`LEFT`, `RIGHT`, `CHARINDEX`, `LEN`) to split single concatenated columns (`ViewsClicksCombined`) into separate `Views` and `Clicks` numeric metrics.
  * Formatted dates into standard `dd.MM.yyyy` string formats and filtered out non-essential content types.

---

## 🐍 Phase 2: Python Natural Language Processing (NLP)

To extract structured insights from unstructured customer review text, a Python pipeline was created using **NLTK (VADER)** and **Pandas**.

### Technical Highlights:
* **Database Connection:** Used `pyodbc` to query `dbo.vw_fact_customer_reviews` directly from Microsoft SQL Server into a Pandas DataFrame.
* **VADER Sentiment Analysis:** Calculated a continuous normalized compound score (ranging from `-1.0` to `+1.0`) for every review text string.
* **Hybrid Classification Logic:** Combined text sentiment scores with numerical star ratings (`1–5`) to handle edge cases like sarcasm (e.g., low rating paired with sarcastic positive phrasing).
* **Dimensional Bucketing:** Segmented continuous compound scores into four categorical ranges (`0.5 to 1.0`, `0.0 to 0.49`, `-0.49 to 0.0`, `-1.0 to -0.5`) to allow dynamic filtering in Power BI.
* **Data Export:** Exported the enriched dataset to `fact_customer_reviews_with_sentiment.csv`.

---

## 📊 Phase 3: Power BI Dashboard (Next Step)
* Building a Star-Schema data model connecting dimension and fact tables.
* Creating DAX measures for Customer Acquisition Cost (CAC), Conversion Rate, and Sentiment Distribution.
* Designing interactive executive dashboards for stakeholder decision-making.