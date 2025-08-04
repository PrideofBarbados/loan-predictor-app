# loan-predictor-app
A Streamlit-based web application that predicts a farmer’s loan eligibility using machine learning. It evaluates financial behavior, farming practices, and climate risk to determine the likelihood of default.
# Farmer Loan Predictor App

This is a Streamlit-based machine learning application that predicts **loan eligibility for farmers** based on various financial, farming, and climate-related factors.

## About the Project

The app uses a trained model (Logistic Regression or Decision Tree) to determine whether a farmer is likely to default on a loan. The predictions help lenders and agricultural institutions make informed, risk-aware decisions.

##Features

- Predict loan default for **individual farmer entries** or **bulk CSV uploads**
- Displays **eligibility messages** alongside farmer IDs
- Accepts and transforms key features like:
  - Location
  - Farm Size (ha)
  - Loan Purpose
  - Mobile Money Score
  - Coop Membership
  - Climate Risk Score
  - Planting Date
  - Repayment Score
  - Loan Amount (₦)

## Input Options

1. **Manual Entry** – Fill a form for a single farmer
2. **Upload CSV** – Predict for multiple farmers at once  
   Ensure your CSV contains:
   - `Farmer ID`
   - All required features listed above

## How to Run Locally
**Clone the repository:**
   git clone https://github.com/PrideofBarbados/loan-predictor-app.git
   cd loan-predictor-app
**install dependencies:**
   pip install -r requirements.txt
**run the app:**
   streamlit run app.py

