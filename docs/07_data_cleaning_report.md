# Data Cleaning Report

This report summarizes the impact of the data cleaning pipeline implemented in [src/02_data_cleaning.py](src/02_data_cleaning.py) on the raw Online Retail dataset.

All figures below are derived from [data/processed/cleaning_statistics.json](data/processed/cleaning_statistics.json).

## 1. Overall impact

- Original rows: **541,910**
- Rows after cleaning: **333,234**
- Rows removed: **208,676**
- Retention rate: **61.49%**

After cleaning, there are **no missing values** in any column used for modelling or feature engineering.

## 2. Step-by-step cleaning summary

The table below shows how many rows were removed at each step of the pipeline. Counts are taken from `steps_applied` in cleaning_statistics.json.

| Step                       | Rows removed |
|---------------------------|-------------:|
| load_data                 |          0   |
| remove_missing_customer_ids |    135,080 |
| handle_cancelled_invoices |      8,905 |
| handle_negative_quantities |          0 |
| handle_zero_prices        |         40 |
| handle_missing_descriptions |        0 |
| remove_outliers           |     59,734 |
| remove_duplicates         |      4,917 |
| add_derived_columns       |          0 |
| convert_data_types        |          0 |

The cumulative effect of these steps matches the reported `rows_removed` total of **208,676**.

## 3. Data quality improvements

Before cleaning:

- Missing values:
	- **CustomerID** missing in **135,080** rows (~24.9%).
	- **Description** missing in **1,454** rows (~0.27%).
- Duplicates: **4,917** exact duplicate rows.
- Negative quantities: **10,624** rows.
- Cancelled invoices (credit notes): **8,905** rows.

After cleaning:

- All rows have a valid **CustomerID** and **Description**.
- No rows remain with negative or zero **Quantity** or **UnitPrice**.
- All known cancelled invoices and exact duplicates have been removed.
- Additional extreme outliers in **Quantity** and **UnitPrice** have been filtered using an IQR-based rule.

## 4. Readiness for modelling

The cleaned dataset [data/processed/cleaned_transactions.csv](data/processed/cleaned_transactions.csv):

- Contains only valid, completed transactions with consistent customer identifiers.
- Is free from missing values and obvious data errors.
- Includes derived columns (`TotalPrice`, `Year`, `Month`, `DayOfWeek`, `Hour`) required for feature engineering.

This dataset is therefore suitable for building the customer-level churn prediction features used in later phases of the project.