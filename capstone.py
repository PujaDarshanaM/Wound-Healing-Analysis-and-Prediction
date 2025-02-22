import streamlit as st
import requests

st.title(" Wound Healing Prediction App")
st.write("Upload your CCD/C-CDA File for Analysis")

# File upload
uploaded_file = st.file_uploader("Upload your CCD/C-CDA file", type=["xml", "json"])

if uploaded_file:
    st.success("File uploaded successfully!")

    # Send file to the Node.js API
    files = {"ccd": uploaded_file.getvalue()}
    response = requests.post("http://localhost:5000/parse_ccd", files=files)

    if response.status_code == 200:
        try:
            data = response.json()

        except Exception as e:  # Make sure 'except' exists
            st.error(f"⚠️ Error parsing API response: {e}")

        #print raw response to streamlit
        st.subheader("Debug: Raw Backend Response")
        st.json(data)  # This will display the full JSON response from Node.js

        # Extract patient information
        patient = data.get("patient", {})
        allergies = data.get("allergies", [])
        medications = data.get("medications", [])
        diagnoses = data.get("diagnoses", [])

        st.subheader("Extracted Patient Information")
        st.write(f"**Name:** {patient.get('name', 'Unknown')}")
        st.write(f"**DOB:** {patient.get('dob', 'N/A')}")
        st.write(f"**Gender:** {patient.get('gender', 'Unknown')}")

        st.subheader("🩺 Clinical Data")
        st.write(f"**Allergies:** {', '.join([str(a.get('name', 'Unknown')) for a in allergies if isinstance(a, dict)]) if allergies else 'No allergies found'}")
        st.write(f"**Medications:** {', '.join([str(m.get('name', 'Unknown')) for m in medications if isinstance(m, dict)]) if medications else 'No medications found'}")
        st.write(f"**Diagnoses:** {', '.join([str(d.get('name', 'Unknown')) for d in diagnoses if isinstance(d, dict)]) if diagnoses else 'No diagnoses found'}")


else:
        st.error(f"❌ Error: {response.json().get('error', 'Unknown error')}")