import duckdb
import pandas as pd

con = duckdb.connect()

df = pd.read_excel("Dataset_Cleaned.xlsx")
con.register("orders", df)

SEP = "\n" + "─" * 60

def run(title, sql):
    print(f"{SEP}\n📌 {title}\n")
    result = con.execute(sql).df()
    print(result.to_string(index=False))
    return result

# ── 1. Basic overview ─────────────────────────────────────────────────────────
run("1. Dataset overview — basic aggregations","""
SELECT
    COUNT(*)                        AS total_orders,
    COUNT(DISTINCT CustomerID)      AS unique_customers,
    COUNT(DISTINCT Product)         AS product_types,
    ROUND(SUM(TotalPrice), 2)       AS total_revenue,
    ROUND(AVG(TotalPrice), 2)       AS avg_order_value,
    ROUND(MEDIAN(TotalPrice), 2)    AS median_order_value,
    MIN(Date)::DATE                 AS first_order,
    MAX(Date)::DATE                 AS last_order
FROM orders
""")

# ── 2. Revenue & orders by product (GROUP BY + aggregations) ─────────────────
run("2. Revenue & orders by product — GROUP BY, SUM, AVG, COUNT","""
SELECT
    Product,
    COUNT(*)                        AS total_orders,
    ROUND(SUM(TotalPrice), 2)       AS total_revenue,
    ROUND(AVG(TotalPrice), 2)       AS avg_order_value,
    ROUND(AVG(UnitPrice), 2)        AS avg_unit_price,
    ROUND(SUM(TotalPrice) * 100.0
        / SUM(SUM(TotalPrice)) OVER (), 1) AS revenue_pct
FROM orders
GROUP BY Product
ORDER BY total_revenue DESC
""")

# ── 3. Order status breakdown ─────────────────────────────────────────────────
run("3. Order status distribution — GROUP BY, COUNT, WHERE","""
SELECT
    OrderStatus,
    COUNT(*)                            AS order_count,
    ROUND(COUNT(*) * 100.0 / 1200, 1)  AS pct_of_total,
    ROUND(AVG(TotalPrice), 2)           AS avg_order_value,
    ROUND(SUM(TotalPrice), 2)           AS total_value
FROM orders
GROUP BY OrderStatus
ORDER BY order_count DESC
""")

# ── 4. High-value orders — WHERE + ORDER BY ───────────────────────────────────
run("4. Top 10 highest-value orders — WHERE, ORDER BY, SELECT","""
SELECT
    OrderID,
    CustomerID,
    Product,
    Quantity,
    UnitPrice,
    TotalPrice,
    OrderStatus,
    PaymentMethod
FROM orders
WHERE TotalPrice > 3000
ORDER BY TotalPrice DESC
LIMIT 10
""")

# ── 5. Monthly revenue trend ──────────────────────────────────────────────────
run("5. Monthly revenue trend — GROUP BY date part, ORDER BY","""
SELECT
    STRFTIME(Date, '%Y-%m')             AS month,
    COUNT(*)                            AS orders,
    ROUND(SUM(TotalPrice), 2)           AS revenue,
    ROUND(AVG(TotalPrice), 2)           AS avg_order_value
FROM orders
GROUP BY month
ORDER BY month
""")

# ── 6. Year-over-year comparison ──────────────────────────────────────────────
run("6. Year-over-year performance — GROUP BY, aggregations","""
SELECT
    YEAR(Date)                          AS year,
    COUNT(*)                            AS total_orders,
    ROUND(SUM(TotalPrice), 2)           AS total_revenue,
    ROUND(AVG(TotalPrice), 2)           AS avg_order_value,
    ROUND(AVG(Quantity), 2)             AS avg_quantity
FROM orders
GROUP BY year
ORDER BY year
""")

# ── 7. Coupon code impact ─────────────────────────────────────────────────────
run("7. Coupon code impact on revenue — GROUP BY, AVG, SUM","""
SELECT
    CouponCode,
    COUNT(*)                            AS uses,
    ROUND(AVG(TotalPrice), 2)           AS avg_order_value,
    ROUND(SUM(TotalPrice), 2)           AS total_revenue,
    ROUND(AVG(Quantity), 2)             AS avg_quantity
FROM orders
GROUP BY CouponCode
ORDER BY avg_order_value DESC
""")

# ── 8. Referral source performance ───────────────────────────────────────────
run("8. Referral source performance — GROUP BY, ORDER BY AVG","""
SELECT
    ReferralSource,
    COUNT(*)                            AS total_orders,
    ROUND(AVG(TotalPrice), 2)           AS avg_order_value,
    ROUND(SUM(TotalPrice), 2)           AS total_revenue,
    ROUND(AVG(CartSize), 2)             AS avg_cart_size
FROM orders
GROUP BY ReferralSource
ORDER BY avg_order_value DESC
""")

# ── 9. Payment method breakdown ───────────────────────────────────────────────
run("9. Payment method breakdown — GROUP BY, COUNT, SUM","""
SELECT
    PaymentMethod,
    COUNT(*)                            AS order_count,
    ROUND(SUM(TotalPrice), 2)           AS total_revenue,
    ROUND(AVG(TotalPrice), 2)           AS avg_order_value
FROM orders
GROUP BY PaymentMethod
ORDER BY total_revenue DESC
""")

# ── 10. Delivered orders only — WHERE filter ──────────────────────────────────
run("10. Delivered orders analysis — WHERE, GROUP BY, AVG","""
SELECT
    Product,
    COUNT(*)                            AS delivered_orders,
    ROUND(AVG(TotalPrice), 2)           AS avg_order_value,
    ROUND(SUM(TotalPrice), 2)           AS delivered_revenue
FROM orders
WHERE OrderStatus = 'Delivered'
GROUP BY Product
ORDER BY delivered_orders DESC
""")

# ── 11. Cart size vs spend buckets ────────────────────────────────────────────
run("11. Cart size spend buckets — CASE, GROUP BY, AVG","""
SELECT
    CASE
        WHEN CartSize BETWEEN 1 AND 3  THEN 'Small  (1–3)'
        WHEN CartSize BETWEEN 4 AND 6  THEN 'Medium (4–6)'
        WHEN CartSize BETWEEN 7 AND 10 THEN 'Large  (7–10)'
    END                                 AS cart_bucket,
    COUNT(*)                            AS orders,
    ROUND(AVG(TotalPrice), 2)           AS avg_order_value,
    ROUND(SUM(TotalPrice), 2)           AS total_revenue
FROM orders
GROUP BY cart_bucket
ORDER BY avg_order_value
""")

# ── 12. Outliers — WHERE with subquery ────────────────────────────────────────
run("12. Statistical outliers — WHERE with subquery (IQR method)","""
WITH stats AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY TotalPrice) AS q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY TotalPrice) AS q3
    FROM orders
),
bounds AS (
    SELECT q1, q3, (q3 - q1) * 1.5 AS iqr,
           q1 - (q3 - q1) * 1.5    AS lower_bound,
           q3 + (q3 - q1) * 1.5    AS upper_bound
    FROM stats
)
SELECT
    o.OrderID,
    o.Product,
    o.Quantity,
    o.UnitPrice,
    o.TotalPrice,
    o.OrderStatus
FROM orders o, bounds b
WHERE o.TotalPrice > b.upper_bound
   OR o.TotalPrice < b.lower_bound
ORDER BY o.TotalPrice DESC
""")

# ── 13. Top customers by spend ────────────────────────────────────────────────
run("13. Top 10 customers by total spend — GROUP BY, SUM, ORDER BY","""
SELECT
    CustomerID,
    COUNT(*)                            AS total_orders,
    ROUND(SUM(TotalPrice), 2)           AS total_spent,
    ROUND(AVG(TotalPrice), 2)           AS avg_order_value,
    COUNT(DISTINCT Product)             AS products_bought
FROM orders
GROUP BY CustomerID
ORDER BY total_spent DESC
LIMIT 10
""")

# ── 14. Cancelled/returned orders by product ──────────────────────────────────
run("14. Cancellation & return rate by product — WHERE IN, GROUP BY","""
SELECT
    Product,
    COUNT(*)                                                    AS total_orders,
    SUM(CASE WHEN OrderStatus = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled,
    SUM(CASE WHEN OrderStatus = 'Returned'  THEN 1 ELSE 0 END) AS returned,
    ROUND(
        (SUM(CASE WHEN OrderStatus IN ('Cancelled','Returned') THEN 1 ELSE 0 END)
         * 100.0 / COUNT(*)), 1
    )                                                           AS cancel_return_rate_pct
FROM orders
GROUP BY Product
ORDER BY cancel_return_rate_pct DESC
""")

print(f"\n{SEP}\n✅  All 14 queries completed.\n")
con.close()
