# Feature Dictionary

This dictionary describes the customer-level features in [data/processed/customer_features.csv](data/processed/customer_features.csv). All features are computed from the cleaned transaction data in [data/processed/cleaned_transactions.csv](data/processed/cleaned_transactions.csv) using the temporal churn definition in [docs/08_churn_definition.md](docs/08_churn_definition.md).

`CustomerID` is the primary key and is not listed below.

| Feature                 | Type       | Range (approx.)              | Description |
|-------------------------|-----------|------------------------------|-------------|
| Churn                  | numeric   | 0–1                          | Target label: 1 if the customer purchased in the training period but made no purchases in the 90-day observation window; 0 otherwise. |
| Recency                | numeric   | 0–283 days                   | Days between the training cutoff date and the customer’s last purchase in the training period (lower = more recent). |
| Frequency              | numeric   | 1–125 invoices               | Number of unique invoices (purchases) in the training period. |
| TotalSpent             | numeric   | 1.25–42,751.82               | Total monetary value of all purchases (sum of `TotalPrice`) in the training period. |
| AvgOrderValue          | numeric   | 1.25–166.80                  | Average revenue per invoice in the training period. |
| UniqueProducts         | numeric   | 1–1,048 products             | Number of distinct products (`StockCode`) purchased in the training period. |
| TotalItems             | numeric   | 1–25,216 units               | Total quantity of items purchased across all invoices in the training period. |
| AvgDaysBetweenPurchases | numeric  | 0–223 days                   | Average number of days between successive purchases for the customer in the training period. |
| AvgBasketSize          | numeric   | 1–2,207 items                | Average number of items per invoice (basket size) in the training period. |
| StdBasketSize          | numeric   | 0–895.86 items               | Standard deviation of basket size across the customer’s invoices in the training period (higher = more variability). |
| MaxBasketSize          | numeric   | 1–2,207 items                | Maximum number of items in a single invoice in the training period. |
| PreferredDay           | numeric   | 0–6 (weekday index)          | Most common day of week of the customer’s purchases (0=Monday, …, 6=Sunday). |
| PreferredHour          | numeric   | 7–20 (hour of day)           | Most common hour of day (24h clock) when the customer makes purchases. |
| CountryDiversity       | numeric   | 1–2 countries                | Number of distinct countries from which the customer has placed orders. |
| CustomerLifetimeDays   | numeric   | 0–282 days                   | Number of days between the customer’s first and last purchase in the training period. |
| PurchaseVelocity       | numeric   | ~0.007–17 purchases/day      | Average purchase frequency: `Frequency / (CustomerLifetimeDays + 1)` (higher = more frequent buyer). |
| Purchases_Last30Days   | numeric   | 0–12 invoices                | Number of unique invoices in the 30 days before the training cutoff. |
| Purchases_Last60Days   | numeric   | 0–30 invoices                | Number of unique invoices in the 60 days before the training cutoff. |
| Purchases_Last90Days   | numeric   | 0–44 invoices                | Number of unique invoices in the 90 days before the training cutoff. |
| ProductDiversityScore  | numeric   | ~0.07–1.0                    | Ratio of unique products to total transactions for the customer (1.0 = almost every transaction uses a different product). |
| AvgPricePreference     | numeric   | ~0.30–6.95                   | Average unit price of items purchased by the customer, capturing their typical price band. |
| StdPricePreference     | numeric   | 0–3.32                       | Standard deviation of unit prices across the customer’s purchases (higher = more varied price sensitivity). |
| MinPrice               | numeric   | 0.001–6.95                   | Lowest unit price paid by the customer. |
| MaxPrice               | numeric   | 0.38–7.50                    | Highest unit price paid by the customer. |
| AvgQuantityPerOrder    | numeric   | 1–2,207 items                | Average number of items per invoice for the customer. |
| RecencyScore           | numeric   | 1–4                          | Quartile-based score (4=most recent, 1=least recent) derived from `Recency`. |
| FrequencyScore         | numeric   | 1–4                          | Quartile-based score (4=most frequent, 1=least frequent) derived from `Frequency`. |
| MonetaryScore          | numeric   | 1–4                          | Quartile-based score (4=highest spenders, 1=lowest) derived from `TotalSpent`. |
| RFM_Score              | numeric   | 3–12                         | Sum of Recency, Frequency, and Monetary scores (`RecencyScore + FrequencyScore + MonetaryScore`), capturing overall customer value. |
| CustomerSegment        | categorical | Champions/Loyal/Potential/At Risk/Lost | RFM-based customer segment: Champions (highest value and most recent), Loyal, Potential, At Risk, or Lost (low value and/or long since last purchase). |

These features are used together to train the churn prediction model and provide interpretable signals about customer behaviour and value.