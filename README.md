# 📊 E-commerce Customer Churn Prediction System

## 1. Project Overview

Customer churn is a major challenge for e-commerce businesses. Retaining existing customers is significantly more cost-effective than acquiring new ones. Therefore, identifying customers who are likely to stop purchasing from the platform is critical for business success.

This project develops a **machine learning-based customer churn prediction system** that analyzes customer purchasing behavior and predicts whether a customer is likely to churn.

The system uses customer transaction data to generate behavioral features such as **Recency, Frequency, Monetary value (RFM)** and other derived metrics. Multiple machine learning models are trained and evaluated, and the best-performing model is deployed through a **Streamlit web application**.

The deployed application allows users to interact with the churn prediction model through an easy-to-use interface.

---

# 2. Project Objectives

The primary goals of this project are:

• Build an end-to-end machine learning pipeline for churn prediction  
• Perform data cleaning and preprocessing on customer transaction data  
• Generate meaningful features that capture customer behavior  
• Train and evaluate multiple machine learning models  
• Select the best model based on performance metrics  
• Deploy the model as an interactive web application using Streamlit  

This system can help businesses **identify at-risk customers early and implement retention strategies**.

---

# 3. Dataset Description

The dataset used in this project contains **e-commerce customer transaction data**. It includes information about customer purchases such as product details, quantities, transaction time, and customer identifiers.

### Important columns in the dataset include:

| Column | Description |
|------|-------------|
| Invoice | Unique transaction ID |
| StockCode | Product identifier |
| Description | Product name |
| Quantity | Number of items purchased |
| InvoiceDate | Date and time of purchase |
| Price | Price per item |
| Customer ID | Unique customer identifier |
| Country | Customer location |

From this dataset, customer-level behavioral features were engineered to support churn prediction.

---

# 4. Machine Learning Pipeline

The project follows a structured machine learning pipeline consisting of multiple stages.

## 4.1 Data Acquisition

Raw transaction data is collected and stored in the `data/raw` directory. This dataset serves as the starting point for the entire pipeline.

---

## 4.2 Data Cleaning

Data cleaning involves several steps:

• Removing invalid transactions  
• Handling missing values  
• Filtering negative quantities or prices  
• Converting date fields into usable formats  

Cleaned data
