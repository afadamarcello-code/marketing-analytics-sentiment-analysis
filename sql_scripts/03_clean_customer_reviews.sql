CREATE VIEW dbo.vw_customer_reviews AS


--********************************

SELECT
reviewID,
customerID,
productID,
ReviewDate,
Rating,
REPLACE(ReviewText, '  ', ' ') as ReviewText

FROM

dbo.customer_reviews;