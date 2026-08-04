import pandas as pd
import pyodbc
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def fetch_data_from_sql ():
    conn_strr = (
        "driver={sql server};"
        "server=localhost\\SQLEXPRESS;"
        "database=PortfolioProject_MarketingAnalytics;"
        "Trusted_connection = yes;"
    )

    conn = pyodbc.connect(conn_strr)
    query = "Select reviewID, customerID, productID, ReviewDate, Rating, ReviewText FROM vw_customer_reviews"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

customer_reviews_df = fetch_data_from_sql()

sia =SentimentIntensityAnalyzer()

def calculate_sentiment(review):
    sentiment =sia.polarity_scores(review)
    return sentiment["compound"]

def cagotrize_sentiment(score, rating):
    if score > 0.05: # Positive sentiment score
        if rating in (5, 4):
            return "Positive" # High rating and positive sentiment
        if rating == 3:
            return "partially positive" # Nuetral rating and postive sentiment
        else:
            return "Partially negative" # Low rating and postive sentiment
    elif score < -0.05: # Negative sentiment score
        if rating <= 2:  # Low rating and Negative sentiment
            return "Negative"
        elif rating == 3: # Nuetral rating and Negative sentiment
            return "Partially negative"
        else:
            return "partially positive" # High rating and Negative sentiment
    else: # Neutral sentiment score
        if rating >= 4:
            return "Positive"
        elif rating == 3:
            return "Neutral"
        else:
            return "Negative"

def sentiment_bucket(score):
    if score >=0.5:
        return "Strongly Postive (0.50 to 1.00)"
    elif 0.05 <= score < 0.5:
        return "Mildly Postive (0.05 to 0.50)"
    elif -0.05 <= score < 0.05:
        return "Neutral (-0.05 to 0.05)"
    elif  -0.5<= score < -0.05:
            return "Mildly Negative (-0.5 to -0.05)"
    else:
       
        return "Strongly Negative (-1.00 to -0.5)"

customer_reviews_df["SentimentScore"] = customer_reviews_df["ReviewText"].apply(calculate_sentiment)
customer_reviews_df["SentimentCategory"] = customer_reviews_df.apply(lambda row:cagotrize_sentiment(row["SentimentScore"],row["Rating"]), axis=1)
customer_reviews_df["SentimentBucket"] = customer_reviews_df["SentimentScore"].apply(sentiment_bucket)

customer_reviews_df.to_csv("fact_customer_reviews_with_sentiment.csv", index=False)
        
