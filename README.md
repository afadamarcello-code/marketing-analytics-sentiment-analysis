# 📈 Marketing Analytics & Customer Sentiment Analysis

## 📌 Project Overview
This project models an enterprise-level Marketing Analytics pipeline. It transforms raw, fragmented customer, product, and campaign data into structured database views, performs Natural Language Processing (NLP) sentiment analysis on customer reviews, and models data into an interactive executive dashboard.

The goal is to analyze marketing efficiency, customer journey bottlenecks, and product feedback to deliver actionable, ROI-focused business strategies.

---

## 🗂️ Project Repository Structure

```text
marketing-analytics-portfolio/
│
├── data/                             # Raw datasets in CSV format
│   ├── raw_customers.csv
│   ├── raw_customer_journey.csv
│   ├── raw_customer_reviews.csv
│   ├── raw_engagement_data.csv
│   ├── raw_geography.csv
│   └── raw_products.csv
│
├── sql_scripts/                      # T-SQL Cleaning & View Creation
│   ├── 01_clean_customers.sql
│   ├── 02_clean_products.sql
│   ├── 03_clean_customer_reviews.sql
│   ├── 04_clean_customer_journey.sql
│   └── 05_clean_engagement_data.sql
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

## 🧹 SQL Data Cleaning & Transformation Layer

To ensure efficient staging and downstream analysis, the raw database tables were cleaned and converted into modular database views (`dbo.vw_*`). 

### Key SQL Cleaning Logic Implemented:
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

## 🚀 Next Steps
* **Phase 2 (Python):** Sentiment analysis on review text (`vw_fact_customer_reviews`) using VADER / NLP libraries.
* **Phase 3 (Power BI):** Star-schema modeling, advanced DAX measures, and interactive executive reporting.