from datetime import datetime

print ("hello world")

import streamlit as st
from lxml import etree
import io

st.title("Wound Healing Prediction App")
st.write("Upload your CCD/C-CDA File")

uploaded_file = st.file_uploader("Upload your CCD/C-CDA file", type=["xml", "json"])

if uploaded_file:
    st.success("File uploaded successfully!")

    # Convert uploaded file to a readable format for etree.parse()
    file_contents = uploaded_file.getvalue()
    file_io = io.BytesIO(file_contents)

    try:
        # Parse the XML with lxml (handles namespaces better)
        tree = etree.parse(file_io)
        root = tree.getroot()

        # CCD/CDA documents use namespaces, get the namespace dictionary
        namespaces = {'cda': 'urn:hl7-org:v3'}

        # Extract Patient Name
        patient_element = root.find(".//cda:recordTarget/cda:patientRole/cda:patient/cda:name", namespaces)
        if patient_element is not None:
            given_name = patient_element.find("cda:given", namespaces)
            family_name = patient_element.find("cda:family", namespaces)
            extracted_name = f"{given_name.text if given_name is not None else 'Unknown'} {family_name.text if family_name is not None else ''}".strip()
        else:
            extracted_name = "Unknown"

        # Extract Date of Birth and Convert to MM/DD/YYYY format
        birth_time_element = root.find(".//cda:patientRole/cda:patient/cda:birthTime", namespaces)
        if birth_time_element is not None and birth_time_element.get("value"):
            dob_raw = birth_time_element.get("value")  # Expected format: YYYYMMDD
            extracted_dob = datetime.strptime(dob_raw, "%Y%m%d").strftime("%m/%d/%Y")
        else:
            extracted_dob = "N/A"

        # Extract Gender
        gender_element = root.find(".//cda:patientRole/cda:patient/cda:administrativeGenderCode", namespaces)
        extracted_gender = gender_element.get("code") if gender_element is not None else "Unknown"

        # Extract Diagnosis
        diagnosis_element = root.find(".//cda:section/cda:entry/cda:observation/cda:code", namespaces)
        extracted_diagnosis = diagnosis_element.get(
            "displayName") if diagnosis_element is not None else "Unknown Diagnosis"

        # Extract Medications
        medications = [med.get("displayName") for med in root.findall(
            ".//cda:section/cda:entry/cda:substanceAdministration/cda:consumable/cda:manufacturedProduct/cda:manufacturedMaterial/cda:code",
            namespaces) if med.get("displayName")]

        # Extract Allergies
        # Locate the "Allergies" section using code="48765-2"
        allergies_section = None
        for section in root.findall(".//cda:section", namespaces):
            code_element = section.find("cda:code", namespaces)
            if code_element is not None and code_element.get("code") == "48765-2":
                allergies_section = section
                break

        # Extract allergy names and reactions
        allergies = []
        if allergies_section is not None:
            table_rows = allergies_section.findall(".//cda:text/cda:table/cda:tbody/cda:tr", namespaces)
            for row in table_rows:
                name_element = row.find(".//cda:td[@styleCode='xmain']/cda:content/cda:content", namespaces)
                reaction_element = row.find(
                    ".//cda:td[@styleCode='xdetails']/cda:content[@styleCode='xreaction']/cda:content[@ID]", namespaces)

                allergy_name = name_element.text if name_element is not None else "Unknown Allergy"
                allergy_reaction = reaction_element.text if reaction_element is not None else "No reaction specified"

                if allergy_name != "Unknown Allergy":
                    allergies.append(f"{allergy_name} (Reaction: {allergy_reaction})")

        print("Extracted Allergies:", allergies)



        # Function to map extracted data to model features
        def map_to_model_features(name, dob, gender, diagnosis, medications, allergies):
            return {
                "name": name,
                "dob": dob,
                "gender": gender,
                "diagnosis": diagnosis,
                "medications": medications,
                "allergies": allergies
            }


        # Calling the function with extracted data
        mapped_features = map_to_model_features(extracted_name, extracted_dob, extracted_gender, extracted_diagnosis,
                                                medications, allergies)

        # Display extracted patient information
        st.subheader("Extracted Patient Information:")
        st.write(f"**Patient Name:** {mapped_features['name']}")
        st.write(f"**Date of Birth (MM/DD/YYYY):** {mapped_features['dob']}")
        st.write(f"**Gender:** {mapped_features['gender']}")
        st.write(f"**Diagnosis:** {mapped_features['diagnosis']}")
        st.write(
            f"**Medications:** {', '.join(mapped_features['medications']) if mapped_features['medications'] else 'None'}")
        st.write(
            f"**Allergies:** {', '.join(mapped_features['allergies']) if mapped_features['allergies'] else 'None'}")

        # Show structured data
        st.subheader("Mapped Features for Model:")
        st.json(mapped_features)

    except etree.XMLSyntaxError:
        st.error("Error parsing the XML file. Please check the file format.")