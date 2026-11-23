CREATE SCHEMA IF NOT EXISTS iceberg.retail;

CREATE TABLE IF NOT EXISTS iceberg.retail.customers AS
SELECT
    customer_id,
    'Customer ' || CAST(customer_id AS VARCHAR) AS customer_name,
    element_at(ARRAY['North', 'South', 'East', 'West'], (customer_id % 4) + 1) AS region
FROM UNNEST(sequence(1, 200)) AS t(customer_id);

CREATE TABLE IF NOT EXISTS iceberg.retail.products AS
SELECT
    product_id,
    'Product ' || CAST(product_id AS VARCHAR) AS product_name,
    element_at(ARRAY['Electronics', 'Home', 'Office', 'Outdoors', 'Accessories'],
               (product_id % 5) + 1) AS category
FROM UNNEST(sequence(1, 30)) AS t(product_id);

CREATE TABLE IF NOT EXISTS iceberg.retail.orders AS
SELECT
    order_id,
    ((order_id * 17) % 200) + 1 AS customer_id,
    date_add('day', (order_id - 1) % 730, DATE '2024-01-01') AS order_date,
    IF(order_id % 10 = 0, 'cancelled', 'completed') AS status
FROM UNNEST(sequence(1, 2000)) AS t(order_id);

CREATE TABLE IF NOT EXISTS iceberg.retail.order_items AS
SELECT
    order_id,
    line_number,
    ((order_id * 7 + line_number * 11) % 30) + 1 AS product_id,
    ((order_id + line_number) % 4) + 1 AS quantity,
    CAST(20 + (((order_id * 7 + line_number * 11) % 30) + 1) * 3 AS DOUBLE) AS unit_price,
    CAST(12 + (((order_id * 7 + line_number * 11) % 30) + 1) * 1.8 AS DOUBLE) AS unit_cost,
    IF(order_id % 5 = 0, 0.1e0, 0.0e0) AS discount_rate
FROM UNNEST(sequence(1, 2000)) AS orders(order_id)
CROSS JOIN UNNEST(sequence(1, (order_id % 3) + 1)) AS lines(line_number);
