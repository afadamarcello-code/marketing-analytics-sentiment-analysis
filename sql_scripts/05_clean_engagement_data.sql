CREATE VIEW dbo.vw_fact_engagement_data AS
SELECT 
    EngagementID,
    ContentID,
    CampaignID,
    ProductID,
    UPPER(REPLACE(ContentType, 'SocialMedia', 'Social Media')) AS ContentType,
    LEFT(ViewsClicksCombined, CHARINDEX('-', ViewsClicksCombined) - 1) AS Views,
    RIGHT(ViewsClicksCombined, LEN(ViewsClicksCombined) - CHARINDEX('-', ViewsClicksCombined)) AS Clicks,
    FORMAT(CONVERT(date, EngagementDate), 'dd.MM.yyyy') AS EngagementDate
FROM 
    dbo.engagement_data
WHERE 
    ContentType != 'Newsletter';