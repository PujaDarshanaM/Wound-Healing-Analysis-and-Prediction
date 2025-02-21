

from pyccda import CCD
import streamlit as st



st.title("Wound Healing Prediction App")
st.write("Upload your CCD/C-CDA File")

uploaded_file = st.file_uploader("Upload your CCD/C-CDA file below", type=["xml", "json"])

if uploaded_file:
    st.success("File uploaded successfully!")

    # Convert uploaded file to a readable format for etree.parse()
    file_contents = uploaded_file.getvalue().decode("utf-8")

    try:
        # Parse the CDA document
        ccd = CCD(file_contents)

        # Extract patient information
        patient_name = ccd.get_patient_name() or "Unknown"
        dob = ccd.get_patient_dob() or "N/A"
        gender = ccd.get_patient_gender() or "Unknown"

        # Extract structured clinical data
        print("Available Sections in CCD:", ccd.sections.keys())
        st.write("Available Sections in CCD:", list(ccd.sections.keys()))

        medications = ccd.get_medications() or ["No medications found"]
        diagnoses = ccd.get_diagnoses() or ["No diagnoses found"]

        # Display extracted data in Streamlit
        st.subheader("Extracted Patient Information")
        st.write(f"**Patient Name:** {patient_name}")
        st.write(f"**Date of Birth:** {dob}")
        st.write(f"**Gender:** {gender}")

        st.subheader("Clinical Data")
        st.write(f"**Medications:** {', '.join(medications)}")
        st.write(f"**Diagnoses:** {', '.join(diagnoses)}")

    except Exception as e:
        st.error(f"Error processing CDA file: {e}")