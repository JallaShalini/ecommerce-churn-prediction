# Data Dictionary

This data dictionary describes the main columns in the **cleaned transaction dataset** produced by [src/02_data_cleaning.py](src/02_data_cleaning.py) and stored in [data/processed/cleaned_transactions.csv](data/processed/cleaned_transactions.csv).

> Note: The original raw file uses `Customer ID` and `Price`. After cleaning we expose a normalized `CustomerID` column and keep the price information through `Price` and `TotalPrice`.

| Column       | Type        | Description |
|-------------|------------|-------------|
| Invoice      | string      | Invoice identifier for a transaction. Invoices starting with `C` represent cancelled/credit notes and are removed during cleaning. |
| StockCode    | category    | Product (item) code for the purchased product. |
| Description  | string      | Human-readable product description. Rows with missing descriptions are dropped. |
| Quantity     | integer     | Number of units purchased in the transaction; negative or zero quantities are removed. |
| InvoiceDate  | datetime    | Timestamp when the invoice was created. Used to derive time-based features. |
| Price        | float       | Unit price of the product in the given currency; non-positive prices are removed. |
| CustomerID   | integer     | Unique identifier for a customer, derived from the raw `Customer ID` column and present only in cleaned data. |
| Country      | category    | Country where the customer resides. |
| TotalPrice   | float       | Line-level revenue calculated as `Quantity * Price` (or `UnitPrice` where applicable). |
| Year         | integer     | Calendar year extracted from `InvoiceDate`. |
| Month        | integer     | Calendar month (1–12) extracted from `InvoiceDate`. |
| DayOfWeek    | integer     | Day of week extracted from `InvoiceDate` (0=Monday, 6=Sunday). |
| Hour         | integer     | Hour of day (0–23) extracted from `InvoiceDate`. |

Customer-level feature definitions (e.g., `Recency`, `Frequency`, `TotalSpent`, `AvgOrderValue`, `CustomerSegment`) are documented separately in [docs/09_feature_dictionary.md](docs/09_feature_dictionary.md) and correspond to the engineered dataset [data/processed/customer_features.csv](data/processed/customer_features.csv).