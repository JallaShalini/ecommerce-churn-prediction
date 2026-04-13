# Exploratory Data Analysis Insights

This document summarizes the main insights from the feature-level EDA performed in [notebooks/03_feature_eda.ipynb](notebooks/03_feature_eda.ipynb), using plots saved under [visualizations/eda](visualizations/eda).

## Key findings

1. **Overall churn rate is moderately high (~43%)**  
	- The churn distribution plot ([visualizations/eda/01_churn_distribution.png](visualizations/eda/01_churn_distribution.png)) shows that approximately 43% of customers are labelled as churned under the 90‑day definition. This provides a reasonably balanced classification problem (not extremely imbalanced).

2. **Churned customers tend to be more recent but then go silent**  
	- Boxplots of `Recency` by churn ([visualizations/eda/Recency_by_churn.png](visualizations/eda/Recency_by_churn.png)) indicate that churned customers often have higher Recency values (more days since last purchase at the cutoff). This is consistent with the temporal churn definition: customers who stop purchasing in the observation window accumulate higher Recency.

3. **High product diversity is associated with higher churn**  
	- The correlation bar chart ([visualizations/eda/03_top10_corr_with_churn.png](visualizations/eda/03_top10_corr_with_churn.png)) shows `ProductDiversityScore` as one of the most positively correlated features with churn (~0.34). Customers who spread their purchases across many different products are more likely to churn, perhaps reflecting browsing or one‑off gift purchases rather than loyal repeat buying.

4. **Strong negative relationship between customer value and churn**  
	- `RFM_Score`, `CustomerLifetimeDays`, `FrequencyScore`, `MonetaryScore`, `Frequency`, `TotalSpent`, and `UniqueProducts` all have notable negative correlations with churn (see [visualizations/eda/02_correlation_heatmap.png](visualizations/eda/02_correlation_heatmap.png) and [visualizations/eda/03_top10_corr_with_churn.png](visualizations/eda/03_top10_corr_with_churn.png)). High‑value, long‑tenure customers are much less likely to churn.

5. **RFM features clearly separate churned vs active customers**  
	- The RFM boxplots by churn ([visualizations/eda/Frequency_by_churn.png](visualizations/eda/Frequency_by_churn.png), [visualizations/eda/TotalSpent_by_churn.png](visualizations/eda/TotalSpent_by_churn.png), [visualizations/eda/AvgOrderValue_by_churn.png](visualizations/eda/AvgOrderValue_by_churn.png)) show that active customers generally have higher purchase frequency, higher total spend, and higher average order values than churned customers.

6. **Customer segments strongly align with churn risk**  
	- The churn rate by segment plot ([visualizations/eda/06_churn_rate_by_segment.png](visualizations/eda/06_churn_rate_by_segment.png)) shows that **Champions** and **Loyal** customers have very low churn rates, while **At Risk** and **Lost** segments have much higher churn. Segment sizes ([visualizations/eda/07_segment_sizes.png](visualizations/eda/07_segment_sizes.png)) confirm that a minority of customers (Champions/Loyal) contribute disproportionately to stable revenue.

7. **RFM_Score is a strong predictor of churn**  
	- The RFM by churn plot ([visualizations/eda/08_rfm_by_churn.png](visualizations/eda/08_rfm_by_churn.png)) shows that churned customers have significantly lower RFM scores than active customers. Correlation analysis ranks `RFM_Score` as one of the most negatively correlated features with churn (around −0.41).

8. **Temporal activity features (recent purchases) reduce churn risk**  
	- Boxplots for recent activity ([visualizations/eda/10_recent_activity_by_churn.png](visualizations/eda/10_recent_activity_by_churn.png)) show that customers with more purchases in the last 90 days before the cutoff are much less likely to churn. Correlations for `Purchases_Last30Days`, `Purchases_Last60Days`, and `Purchases_Last90Days` are all negative with respect to churn, reinforcing that recent activity is protective.

9. **Purchase velocity differentiates churned vs active customers**  
	- The purchase velocity plot ([visualizations/eda/09_purchase_velocity_by_churn.png](visualizations/eda/09_purchase_velocity_by_churn.png)) and correlation values indicate that customers with very low purchase velocity (few purchases per day of lifetime) are more likely to churn. T‑tests for `PurchaseVelocity` show a statistically significant difference (p < 0.05) between churned and active groups.

10. **Multiple key numeric features show statistically significant differences by churn**  
	- T‑tests run in the notebook for `Recency`, `Frequency`, `TotalSpent`, `RFM_Score`, `ProductDiversityScore`, and `PurchaseVelocity` (see the t‑test cell output in [notebooks/03_feature_eda.ipynb](notebooks/03_feature_eda.ipynb)) produce very low p‑values (p < 0.05). This confirms that these features differ meaningfully between churned and active customers and are strong candidates for the final prediction model.

Overall, the EDA supports using RFM-based value metrics, recent activity windows, purchase velocity, and product diversity as core predictors in the churn model, with customer segment labels providing an interpretable summary of risk levels for business stakeholders.