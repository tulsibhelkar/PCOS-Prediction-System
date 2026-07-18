import streamlit as st
import os

from backend.predictor import predict_pcos
from backend.report_analyzer import analyze_report

st.set_page_config(
    page_title=" PCOS Prediction System",
    page_icon="🩺",
    layout="wide"
)

# ---------------- HEADER ---------------- #

st.title(" PCOS Prediction System")

st.markdown(
"""
This system predicts **PCOS** using:

Hybrid Machine Learning Model (Random Forest + XGBoost)

Report Analysis

---
"""
)


menu = st.sidebar.radio(

    "Choose Option",

    [

        "Clinical Prediction",

        "Upload Ultrasound Report"

    ]

)



if menu == "Clinical Prediction":

    st.header("Clinical Prediction")

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input("Age (yrs)",18,60)

        weight = st.number_input("Weight (Kg)",30,150)

        pregnant = st.selectbox("Pregnant",["No","Yes"])

        abortions = st.number_input("No. of Abortions",0,10)

        weight_gain = st.selectbox("Weight Gain",["No","Yes"])

        hair_growth = st.selectbox("Hair Growth",["No","Yes"])

        skin_dark = st.selectbox("Skin Darkening",["No","Yes"])

        hair_loss = st.selectbox("Hair Loss",["No","Yes"])

    with col2:

        pimples = st.selectbox("Pimples",["No","Yes"])

        fast_food = st.selectbox("Fast Food",["No","Yes"])

        fsh_lh = st.number_input("FSH/LH Ratio",0.0,20.0)

        follicle_l = st.number_input("Follicle No. (L)",0,50)

        follicle_r = st.number_input("Follicle No. (R)",0,50)

        cycle = st.selectbox("Cycle",["Regular","Irregular"])

        cycle_length = st.number_input("Cycle Length",15,90)

    if st.button("Predict PCOS"):

        sample = {

            "Age (yrs)": age,

            "Weight (Kg)": weight,

            "Pregnant(Y/N)": 1 if pregnant=="Yes" else 0,

            "No. of abortions": abortions,

            "Weight gain(Y/N)": 1 if weight_gain=="Yes" else 0,

            "hair growth(Y/N)": 1 if hair_growth=="Yes" else 0,

            "Skin darkening (Y/N)": 1 if skin_dark=="Yes" else 0,

            "Hair loss(Y/N)": 1 if hair_loss=="Yes" else 0,

            "Pimples(Y/N)": 1 if pimples=="Yes" else 0,

            "Fast food (Y/N)": 1 if fast_food=="Yes" else 0,

            "FSH/LH": fsh_lh,

            "Follicle No. (L)": follicle_l,

            "Follicle No. (R)": follicle_r,

            "Cycle(R/I)": 1 if cycle=="Irregular" else 0,

            "Cycle length(days)": cycle_length

        }

        prediction, probability = predict_pcos(sample)

        st.divider()

        st.header("Prediction Result")

        if prediction==1:

            st.error(" PCOS Positive")

        else:

            st.success(" PCOS Negative")

        st.progress(int(probability*100))

        st.write(f"Confidence : **{round(probability*100,2)}%**")



else:

    st.header("Upload Medical Report")

    uploaded = st.file_uploader(

        "Upload PDF / JPG / PNG",

        type=["pdf","png","jpg","jpeg"]

    )

    if uploaded:

        os.makedirs("uploads",exist_ok=True)

        path = os.path.join("uploads",uploaded.name)

        with open(path,"wb") as f:

            f.write(uploaded.getbuffer())

        st.success("Report Uploaded Successfully")

        if st.button("Analyze Report"):

            with st.spinner("Analyzing Report..."):

                positive,confidence,findings,text = analyze_report(path)

            st.divider()

            st.header("Report Analysis")

            if positive:

                st.error(" Report Suggests PCOS")

            else:

                st.success("No Strong PCOS Findings")

            st.subheader("Confidence")

            st.progress(confidence)

            st.write(f"**{confidence}%**")

            st.subheader("Risk Level")

            if confidence>=90:

                st.error("High Risk")

            elif confidence>=70:

                st.warning("Moderate Risk")

            else:

                st.success("Low Risk")

            st.subheader("Detected Findings")

            if len(findings)==0:

                st.write("No PCOS related findings detected.")

            else:

                for item in findings:

                    st.write("✔",item)

            st.subheader("Recommendation")

            if positive:

                st.info("""

✔ Consult Gynecologist

✔ Hormonal Blood Test

✔ Pelvic Ultrasound Follow-up

✔ Healthy Diet

✔ Regular Exercise

""")

            else:

                st.info("""

✔ Maintain Healthy Lifestyle

✔ Annual Checkup

✔ Balanced Diet

""")

            with st.expander("Extracted Report Text"):

                st.write(text)