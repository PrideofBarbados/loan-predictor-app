import streamlit as st
import pandas as pd
import numpy as np
import pickle
pickle_in = open('random_model.pkl','rb')
model = pickle.load(pickle_in)

import streamlit as st
import pandas as pd
import pickle
from datetime import datetime

# Load trained model
with open("random_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title('FARMER CREDIT SCORE MODEL')
st.markdown("Check loan eligibility based on financial and farming behavior — upload a file or enter one farmer's info.")

# Mapping dictionaries
location_map = {"North": 0, "South": 1, "East": 2, "West": 3}
loan_purpose_map = {"Fertilizer": 0, "Seeds": 1, "Machinery": 2, "Irrigation": 3, "Other": 4}
coop_map = {"Yes": 1, "No": 0}

required_features = [
    "Location", "Farm Size (ha)", "Loan Purpose", "Mobile Money Score",
    "Coop Membership", "Climate Risk Score", "Planting Date",
    "Repayment Score", "Loan Amount (₦)"
]

input_mode = st.radio("Select input method:", ["Manual Entry", "Upload CSV"])

# File upload mode
if input_mode == "Upload CSV":
    file = st.file_uploader("Upload CSV with correct columns", type=["csv"])
    if file:
        df = pd.read_csv(file)

        if "Farmer ID" not in df.columns:
            st.error("Your CSV must include a 'Farmer ID' column.")
        else:
            missing_cols = [col for col in required_features if col not in df.columns]
            if missing_cols:
                st.error(f"Missing columns: {', '.join(missing_cols)}")
            else:
                # Map values if needed
                if df["Location"].dtype == object:
                    df["Location"] = df["Location"].map(location_map)
                if df["Loan Purpose"].dtype == object:
                    df["Loan Purpose"] = df["Loan Purpose"].map(loan_purpose_map)
                if df["Coop Membership"].dtype == object:
                    df["Coop Membership"] = df["Coop Membership"].map(coop_map)
                if "Planting Date" in df.columns:
                    df["Planting Date"] = pd.to_datetime(df["Planting Date"]).astype(int) / 10**9

                X = df[required_features]
                predictions = model.predict(X)
                df["Default_Prediction"] = predictions

                st.success("✅ Predictions complete!")
                st.dataframe(df)

                for _, row in df.iterrows():
                    msg = f"🧑‍🌾 Farmer ID {row['Farmer ID']} - "
                    if row["Default_Prediction"] == 1:
                        st.error(msg + "❌ Not Eligible for Loan")
                    else:
                        st.success(msg + "✅ Eligible for Loan")

# Manual input mode
else:
    st.subheader("Enter Single Farmer Details")
    farmer_id = st.text_input("Farmer ID")

    location = st.selectbox("Location", list(location_map.keys()))
    farm_size = st.number_input("Farm Size (ha)", min_value=0.1, max_value=200.0, step=0.1)
    loan_purpose = st.selectbox("Loan Purpose", list(loan_purpose_map.keys()))
    mobile_money_score = st.slider("Mobile Money Score", 0.0, 1.0, 0.5)
    coop_membership = st.selectbox("Coop Membership", list(coop_map.keys()))
    climate_risk_score = st.slider("Climate Risk Score", 0.0, 1.0, 0.5)
    planting_date = st.date_input("Planting Date")
    repayment_score = st.slider("Repayment Score", 0.0, 1.0, 0.5)
    loan_amount = st.number_input("Loan Amount (₦)", min_value=10000.0, max_value=500000.0, step=5000.0)

    if st.button("Predict"):
        data = {
            "Location": location_map[location],
            "Farm Size (ha)": farm_size,
            "Loan Purpose": loan_purpose_map[loan_purpose],
            "Mobile Money Score": mobile_money_score,
            "Coop Membership": coop_map[coop_membership],
            "Climate Risk Score": climate_risk_score,
            "Planting Date": int(datetime.strptime(str(planting_date), "%Y-%m-%d").timestamp()),
            "Repayment Score": repayment_score,
            "Loan Amount (₦)": loan_amount
        }

        input_df = pd.DataFrame([data])
        result = model.predict(input_df)[0]

        if result == 1:
            st.error(f"🧑‍🌾 Farmer ID {farmer_id} - ❌ Not Eligible for Loan")
        else:
            st.success(f"🧑‍🌾 Farmer ID {farmer_id} - ✅ Eligible for Loan")