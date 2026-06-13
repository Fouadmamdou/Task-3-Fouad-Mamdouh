# Task-3
## 🗄️ SQL Analysis — Extracted Insights

> Queries written in **DuckDB SQL** and executed via Python on the cleaned dataset (1,200 orders · 15 columns · Jan 2023–Jun 2025).

---

### 📊 1. Dataset at a Glance

| Metric | Value |
|---|---|
| Total Orders | 1,200 |
| Unique Customers | 1,189 |
| Total Revenue | $1,264,762 |
| Mean Order Value | $1,054 |
| Median Order Value | $824 |
| Date Range | 2023-01-01 → 2025-06-30 |

> Mean vs median gap ($230) confirms a **right-skewed** distribution — a small number of large orders inflate the average.

---

### 📦 2. Revenue by Product

| Product | Orders | Revenue | Avg Order Value | Revenue Share |
|---|---|---|---|---|
| Chair | 178 | $195,620 | $1,099 | 15.5% |
| Printer | 181 | $195,613 | $1,081 | 15.5% |
| Laptop | 173 | $192,127 | **$1,111 ← highest AOV** | 15.2% |
| Tablet | 179 | $186,569 | $1,042 | 14.8% |
| Monitor | 163 | $175,651 | $1,078 | 13.9% |
| Desk | 170 | $167,460 | $985 | 13.2% |
| Phone | 156 | $151,722 | **$973 ← lowest AOV** | 12.0% |

> Revenue is evenly distributed across all 7 categories (12–15.5%). No single product carries the business — a sign of a **balanced catalog**.

---

### ⚠️ 3. Order Status — Critical Finding

| Status | Count | Share | Avg Order Value |
|---|---|---|---|
| Cancelled | 250 | 20.8% | $1,106 |
| Returned | 247 | 20.6% | $985 |
| Pending | 237 | 19.8% | $1,082 |
| Shipped | 235 | 19.6% | $1,047 |
| Delivered | 231 | 19.3% | $1,050 |

> 🚨 **Only 19.3% of orders are delivered.** Cancel + return rate is **41.4%** — far above the healthy e-commerce benchmark of <10%. This is the most critical operational issue in the dataset.

---

### 📅 4. Year-over-Year Decline

| Year | Orders | Revenue | Avg Order Value | Avg Quantity |
|---|---|---|---|---|
| 2023 | 510 | $552,643 | $1,084 | 2.99 |
| 2024 | 459 | $480,236 | $1,046 | 2.94 |
| 2025* | 231 | $231,883 | $1,004 | 2.86 |

*\*2025 is a partial year (Jan–Jun only)*

> Orders, revenue, AOV, and average quantity **all declined** year-over-year — a consistent downward trend across every key metric.

---

### 🛒 5. Cart Size Drives Revenue

| Cart Bucket | Orders | Avg Order Value | Total Revenue |
|---|---|---|---|
| Small (1–3 items) | 251 | $599 | $150,298 |
| Medium (4–6 items) | 544 | $1,011 | $549,811 |
| Large (7–10 items) | 405 | **$1,394** | **$564,653** |

> Large-cart customers spend **2.3× more per order** than small-cart customers and generate the most total revenue despite not being the largest group. **Upsell and cross-sell strategies targeting active browsers are the clearest revenue opportunity.**

---

### 💳 6. Payment Method — Hidden AOV Difference

| Method | Orders | Avg Order Value | Total Revenue |
|---|---|---|---|
| Credit Card | 234 | **$1,128 ← highest** | $263,848 |
| Gift Card | 230 | $1,071 | $246,324 |
| Cash | 246 | $1,056 | $259,786 |
| Online | 258 | $1,017 | $262,443 |
| Debit Card | 232 | **$1,002 ← lowest** | $232,361 |

> Credit Card users spend **12.6% more per order** than Debit Card users despite similar order counts — a potential target segment for premium product promotions.

---

### 📣 7. Referral Source Performance

| Source | Orders | Avg Order Value | Total Revenue | Avg Cart Size |
|---|---|---|---|---|
| Facebook | 228 | **$1,098** | $250,411 | 5.33 |
| Instagram | 259 | $1,063 | $275,285 | 5.50 |
| Email | 250 | $1,047 | $261,809 | 5.60 |
| Google | 241 | $1,039 | $250,441 | 5.57 |
| Referral | 222 | $1,022 | $226,816 | 5.40 |

> **Facebook drives the highest AOV ($1,098)** — 7.5% above peer referrals. Instagram brings the most orders (259) with strong AOV. Social channels consistently outperform search and word-of-mouth on spend per order.

---

### 🏷️ 8. Coupon Code Impact

| Coupon | Uses | Avg Order Value | Total Revenue |
|---|---|---|---|
| FREESHIP | 313 | **$1,070** | $335,037 |
| SAVE10 | 286 | $1,066 | $304,840 |
| No Coupon | 309 | $1,043 | $322,401 |
| WINTER15 | 292 | $1,036 | $302,484 |

> Coupon users actually spend **slightly more** than non-coupon users on average. `FREESHIP` drives the most revenue of any code — free shipping may encourage customers to add more items.

---

### 🔍 9. Outliers (IQR Method)

All **8 statistical outliers** share the same profile:

- Maximum quantity ordered (Qty = 5)
- High unit price ($667–$691)
- Total order value $3,334–$3,456
- Spread across: Tablet, Monitor, Laptop, Chair, Printer

> These are **legitimate high-value transactions**, not data errors. They represent the natural ceiling of `max_qty × max_price` combinations.

---

### ❌ 10. Cancellation & Return Rate by Product

| Product | Orders | Cancelled | Returned | Cancel+Return Rate |
|---|---|---|---|---|
| Monitor | 163 | 35 | 36 | **43.6% ← worst** |
| Tablet | 179 | 34 | 43 | 43.0% |
| Laptop | 173 | 35 | 39 | 42.8% |
| Chair | 178 | 45 | 28 | 41.0% |
| Printer | 181 | 35 | 38 | 40.3% |
| Phone | 156 | 31 | 31 | 39.7% |
| Desk | 170 | 35 | 32 | **39.4% ← best** |

> Monitor has the highest combined cancel+return rate at 43.6%. Desk is the most reliably fulfilled product at 39.4%. All rates are still alarmingly high — this is a systemic issue, not product-specific.

---

### 🛠️ SQL Concepts Demonstrated

| Concept | Queries Used In |
|---|---|
| `SELECT`, `WHERE`, `ORDER BY` | #4, #10, #12 |
| `GROUP BY` + `COUNT`, `SUM`, `AVG` | #2, #3, #6, #7, #8, #9, #11, #13, #14 |
| `CASE WHEN` (conditional aggregation) | #11, #14 |
| Window functions (`SUM() OVER ()`) | #2 |
| CTEs (`WITH`) + subqueries | #12 |
| Date functions (`STRFTIME`, `YEAR()`) | #5, #6 |
| `PERCENTILE_CONT` (statistical) | #12 |
| `COUNT DISTINCT` | #1, #13 |

---

### 🛠️ Tools
`Python` · `DuckDB` · `pandas` · `openpyxl`
