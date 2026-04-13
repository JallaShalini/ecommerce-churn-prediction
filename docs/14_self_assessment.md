# Self Assessment

## Phase-wise Status & Self-Scores

- **Phase 1 – Business Understanding**  
	Status: Completed  
	Score: 9/10  
	Reason: Business problem, scope, technical approach, and success criteria
	are clearly documented and aligned with the 90-day churn definition.

- **Phase 2 – Data Acquisition & Initial Exploration**  
	Status: Completed  
	Score: 9/10  
	Reason: Raw data is loaded, profiled, and summarized in JSON with the
	required schema; documentation describes dataset size and quality.

- **Phase 3 – Data Cleaning & Validation**  
	Status: Completed  
	Score: 9/10  
	Reason: DataCleaner class implements a reproducible cleaning pipeline and
	produces cleaning_statistics.json; validation notebook checks key
	assumptions.

- **Phase 4 – Feature Engineering & Churn Definition**  
	Status: Completed  
	Score: 9/10  
	Reason: FeatureEngineer class defines churn using a temporal split and
	creates rich customer-level features and feature_info.json.

- **Phase 5 – Feature-level EDA**  
	Status: Completed  
	Score: 8/10  
	Reason: EDA notebook covers distributions, correlations, and t-tests for
	key features; insights are summarized in docs.

- **Phase 6 – Model Development**  
	Status: Completed  
	Score: 9/10  
	Reason: Multiple models are trained and compared, with Logistic Regression
	selected based on validation metrics and stability.

- **Phase 7 – Evaluation, Cross-Validation, Business Impact**  
	Status: Completed  
	Score: 9/10  
	Reason: Test-set metrics and plots are generated; 5-fold CV is performed;
	business impact is quantified using the confusion matrix and realistic
	assumptions.

- **Phase 8 – Deployment (API + Streamlit)**  
	Status: Completed  
	Score: 9/10  
	Reason: Prediction API mirrors training preprocessing; Streamlit app
	includes single and batch prediction, dashboard, and documentation pages.

- **Phase 9 – Documentation & Presentation**  
	Status: Completed  
	Score: 9/10  
	Reason: README, technical documentation, business docs, and a slide
	deck-style presentation file cover all required sections.

- **Phase 10 – Code Quality & Submission**  
	Status: Completed  
	Score: 9/10  
	Reason: Project structure matches the rubric, key scripts have docstrings,
	and submission.json reflects final metrics and deployment details.

## Key Achievements

- Implemented a leakage-free 90-day churn definition using a temporal split
	between training and observation windows.
- Built a reusable data cleaning and feature engineering pipeline with clear
	JSON artifacts for statistics and feature metadata.
- Evaluated multiple models and selected a Logistic Regression model that
	balances performance and interpretability.
- Connected the model to a user-friendly Streamlit app that supports single
	and batch predictions and visualizes evaluation results.
- Documented the full project lifecycle from business understanding to
	deployment and business impact.

## Challenges Faced

- Handling the temporal aspects of churn definition without introducing data
	leakage.
- Managing many intermediate artifacts (CSVs, JSON, plots, models) and
	keeping paths consistent across scripts and notebooks.
- Debugging relative path issues when moving from local scripts to Streamlit
	pages and Dockerized environments.

## Future Improvements

- Add automated unit tests for the data pipeline and prediction API.
- Introduce scheduled model retraining and automatic performance monitoring.
- Explore more advanced calibration and segmentation-specific thresholds for
	churn probability.