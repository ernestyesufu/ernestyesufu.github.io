

---Task: Create a consolidated sales report table by joining order, product, customer, payment, and credit card data.
CREATE TABLE sales_combined_data.sales_report AS
SELECT 
    o.order_id,
    o.order_date,
    
    CAST(regexp_replace(o.quantity, '[^0-9]', '', 'g') AS INTEGER) AS quantity,

    o.product_id,
    p.product_name,
    p.product_category,
    CAST(p.unit_cost AS NUMERIC) AS unit_cost,
    CAST(p.unit_price AS NUMERIC) AS unit_price,
    ROUND(
        CAST(regexp_replace(o.quantity, '[^0-9]', '', 'g') AS INTEGER) * 
        CAST(p.unit_price AS NUMERIC), 
        2
    ) AS total_sales,

    o.customer_id,
    c.customer_name,
    c.email,
    c.city,
    c.country,

    cc.card_number,
    cc.card_expiry_date,
    cc.bank_name,

    pd.payment_id,
    pd.payment_date

FROM 
    sales_combined_data."order_data" o
JOIN 
    sales_combined_data.product_data p ON o.product_id = p.product_id
JOIN 
    sales_combined_data.customers_data c ON o.customer_id = c.customer_id
LEFT JOIN 
    sales_combined_data.credit_card_data cc ON c.customer_id = cc.customer_id
LEFT JOIN 
    sales_combined_data.payment_data pd ON o.order_id = pd.order_id;