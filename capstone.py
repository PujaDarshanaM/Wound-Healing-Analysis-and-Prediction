
import streamlit as st
import requests

st.title("Wound Healing Prediction App")
st.write("Upload your CCD/C-CDA File for Analysis")

# File upload
uploaded_file = st.file_uploader("Upload your CCD/C-CDA file", type=["xml", "json"])

if uploaded_file:
    st.success("✅ File uploaded successfully!")

    # Send file to the Node.js API
    files = {"ccd": uploaded_file.getvalue()}
    try:
        response = requests.post("http://localhost:5000/parse_ccd", files=files)

        if response.status_code == 200:
            data = response.json()

            #Show raw JSON response (To check if Json is extracted correctly)
            st.subheader("Raw Backend Response")
            st.json(data)  # This will display the full JSON response from Node.js

            # Extract patient information
            patient = data.get("patient", {})

            # Patient name extraction
            patient_name = " ".join(patient.get("name", {}).get("given", []) + [patient.get("name", {}).get("family", "Unknown")])

            st.subheader("Extracted Patient Information")
            st.write(f"**Name:** {patient_name}")
            st.write(f"**DOB:** {patient.get('dob', 'N/A')}")
            st.write(f"**Gender:** {patient.get('gender', 'Unknown')}")

            # Function to extract specific fields safely
            def extract_names(items, key="name", subkey=None):
                extracted = []
                for item in items:
                    if isinstance(item, dict):
                        value = item.get(key, "Unknown")
                        if subkey and isinstance(value, dict):
                            value = value.get(subkey, "Unknown")
                        extracted.append(str(value) if value else "Unknown")
                return extracted if extracted else ["No data found"]

            st.subheader("Clinical Data")

            # Fix Allergies Extraction (Extract from `allergen.name`)
            allergies = data.get("allergies", [])
            extracted_allergies = [a.get("allergen", {}).get("name", "Unknown") for a in allergies]
            st.write(f"**Allergies:** {', '.join(extracted_allergies) if extracted_allergies else 'No allergies found'}")

            # Fix Medications Extraction (Extract from `product.name`)
            medications = data.get("medications", [])
            extracted_medications = [m.get("product", {}).get("name", "Unknown") for m in medications]
            st.write(f"**Medications:** {', '.join(extracted_medications) if extracted_medications else 'No medications found'}")

            # Diagnoses (If empty, show 'No diagnoses found')
            diagnoses = data.get("diagnoses", [])
            extracted_diagnoses = [
                str(d.get("name") or d.get("translation", {}).get("name", "Unknown Diagnosis"))
                for d in diagnoses if isinstance(d, dict)
            ]
            st.write(
                f"**Diagnoses:** {', '.join(extracted_diagnoses) if extracted_diagnoses else 'No diagnoses found'}")

        else:
            st.error(f"❌ API Request Failed: {response.status_code} - {response.text}")

    except Exception as e:
        st.error(f"⚠️ Error processing request: {e}")

else:
    st.warning("⚠️ Please upload a CCD file first.")
#to run this app, run the server.js first using node "server.js", then in a new terminal run the app using "streamlit run capstone.py"