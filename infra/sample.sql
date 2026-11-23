CREATE SCHEMA IF NOT EXISTS iceberg.demo;

CREATE TABLE IF NOT EXISTS iceberg.demo.orders AS
SELECT * FROM (
    VALUES
        ('North', 'Laptop', 1200.0),
        ('South', 'Monitor', 300.0),
        ('North', 'Monitor', 250.0),
        ('West', 'Laptop', 1100.0),
        ('South', 'Laptop', 1000.0),
        ('West', 'Monitor', 350.0)
) AS sample (region, product, amount);

SELECT region, sum(amount) AS revenue
FROM iceberg.demo.orders
GROUP BY region
ORDER BY revenue DESC, region;
