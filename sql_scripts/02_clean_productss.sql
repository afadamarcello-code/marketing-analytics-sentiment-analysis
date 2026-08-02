CREATE VIEW dbo.vw_fact_products AS


SELECT

productID,
 productName,
  price,
   case
        WHEN price < 50 then 'Low'
        WHEN price BETWEEN 50 and 200 then 'Medium'
        else 'High'
    End as priceCategory
FROM 
dbo.products    
