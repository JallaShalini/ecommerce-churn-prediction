# Business Impact Analysis

This section translates the model's evaluation metrics into estimated financial impact for the ecommerce business.

## 1. Confusion Matrix and Key Metrics (Test Set)

On the held-out test set, the chosen Logistic Regression model produced the following confusion matrix for churn prediction:

- True negatives (TN): 200 (correctly identified non-churners)
- False positives (FP): 78 (flagged as churners but would not churn)
- False negatives (FN): 71 (missed churners)
- True positives (TP): 138 (correctly identified churners)

From this we obtain:

- Accuracy: ~69%
- Precision: ~64%
- Recall: ~66%
- F1-score: ~0.65
- ROC-AUC: ~0.77

These numbers indicate a model that meaningfully separates churners from non-churners while keeping a reasonable balance between catching churners (recall) and limiting unnecessary interventions (precision).

## 2. Assumptions for Financial Impact

To estimate business impact, we make the following reasonable assumptions for this ecommerce context:

- Average customer annual contribution margin (customer value): $120
- Cost of a targeted retention action (e.g., discount, personalized campaign): $10 per contacted customer
- Probability that a correctly targeted churner (true positive) is saved by the campaign: 25%
- Customers who would not churn but are targeted (false positives) still cost $10 each but do not generate incremental savings

Under these assumptions, we can estimate the net value created by using the model to target at-risk customers.

## 3. Scenario Comparison: With vs. Without Model

### 3.1 Without Model (No Targeting)

If no churn model is used, assume the business does not run a targeted retention campaign. In this case:

- No direct campaign cost
- All churners (TP + FN = 209 customers in the test sample) are lost
- Lost margin from these churners: 209 × $120 = $25,080

### 3.2 With Model-Based Targeting

Using the model, the business targets all customers predicted as churners (TP + FP):

- Customers targeted: TP + FP = 138 + 78 = 216
- Campaign cost: 216 × $10 = $2,160

Among the 138 true churners correctly identified (TP):

- Expected saved churners: 138 × 25% ≈ 35 customers
- Margin retained from these saved customers: 35 × $120 = $4,200

False positives (78 customers) receive the offer but would not have churned; they only add cost:

- Incremental benefit from FPs: $0
- Cost already included in the campaign cost above

Net incremental benefit of using the model vs. no targeting:

- Net gain = retained margin − campaign cost
- Net gain ≈ $4,200 − $2,160 = $2,040 (on the test sample size)

If we scale this to a larger production population (e.g., 10× the test size), the model-driven strategy would be expected to generate roughly 10 × $2,040 = $20,400 in net annualized margin, assuming similar churn mix and behavior.

## 4. Alignment with Business Goals and Success Criteria

The original business goal was to reduce churn while keeping marketing spend efficient. The technical success criteria required a ROC-AUC above 0.75 with balanced precision and recall.

- The model achieves ROC-AUC ~0.77 with F1 ~0.65, satisfying the technical performance thresholds.
- Financially, under conservative assumptions, the model yields a positive net impact by retaining a subset of high-risk customers at a relatively low per-customer campaign cost.

This analysis shows that deploying the churn model to prioritize retention actions is likely to increase customer lifetime value and improve the efficiency of marketing spend, supporting both business and technical success criteria.