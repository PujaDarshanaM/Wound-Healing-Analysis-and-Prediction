Wound Healing Analysis and Prediction
A Data-Driven Approach for Chronic Wound Prognosis Using EHR Data and Temporal Fusion Transformers

📌 Overview
Chronic wounds, such as diabetic foot ulcers and pressure injuries, present significant challenges due to their prolonged healing time and associated healthcare costs. This project addresses the problem by leveraging longitudinal EHR data extracted from Continuity of Care Documents (CCD/C-CDA) and applying advanced time-series modeling techniques for personalized wound healing prediction.

The solution integrates:

Data Preprocessing Pipeline for longitudinal clinical data.

Temporal Fusion Transformer (TFT) for interpretable multi-horizon forecasting.

Streamlit Interface + BlueButton.js Backend for easy visualization and CCD parsing.

✨ Key Features
CCD Parsing: Extracts structured clinical data (demographics, medications, diagnoses, allergies) using BlueButton.js.

Longitudinal Data Handling: Normalizes EHR data into patient-time step sequences for time-series modeling.

Missing Data Imputation: Handles sparse entries using forward-fill and embedding techniques.

Feature Engineering: Creates static and dynamic covariates for machine learning.

TFT Model Integration: Implements Temporal Fusion Transformer for predictive analytics on chronic wound healing.

Interactive Dashboard: Streamlit app for uploading CCD files and viewing parsed outputs.

🔍 Data Handling Pipeline
Managing longitudinal health data requires a structured approach to handle temporal patterns, missingness, and heterogeneous features. Our pipeline includes:

✅ 1. Data Cleaning & Harmonization
Normalized patient records from CCD files into structured time-series format.

Aligned static features (e.g., age, gender) with dynamic variables (e.g., wound size, medications, vitals).

✅ 2. Handling Missing Data
Forward-filling for continuous features.

Embedding indices for categorical variables.

✅ 3. Feature Engineering
Static Features: Patient demographics, comorbidity counts.

Dynamic Features: Clinical observations and treatments over time.

Known Future Inputs: Intervention schedules for conditioning the forecast.

✅ 4. Scaling and Normalization
Standardized numeric features.

Embedded categorical features for deep learning models.

✅ 5. Data Structuring for TFT
Organized in long format with:

time_idx (time steps)

group_id (patient identifier)

Static and dynamic covariates split as per TFT requirements.

🤖 Model: Temporal Fusion Transformer (TFT)
Implemented TFT using PyTorch Forecasting:

Captures short- and long-term dependencies in irregular time series.

Handles static, known, and observed covariates.

Provides interpretability via attention mechanisms.

Goal: Predict wound healing trajectory (e.g., time to healing, risk of non-healing) using patient-specific longitudinal data.

🖥️ App Interface
Built with Streamlit for an intuitive UI.

Allows uploading CCD/C-CDA files and visualizes parsed data.

Backend powered by Node.js and BlueButton.js for CCD parsing.

📊 Future Enhancements
✅ Full integration of TFT predictions into Streamlit dashboard.

✅ Deployment on cloud (AWS, Streamlit Cloud).

✅ Support for FHIR-compliant EHR systems.

