import streamlit as st
import requests
import pandas as pd

st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(
        135deg,
        #eef4ff 0%,
        #f7f9fc 50%,
        #edf6ff 100%
    );
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #1E3A5F;
}

/* Sidebar Text */
[data-testid="stSidebar"] * {
    color: white;
}

/* Cards */
div[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 15px;
    border: 1px solid #dbeafe;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* Input Boxes */
.stTextInput input,
.stNumberInput input,
.stSelectbox {
    border-radius: 10px;
}

/* Button */
.stButton > button {
    background: linear-gradient(
        90deg,
        #2563EB,
        #3B82F6
    );
    color: white;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    font-weight: 600;
    border: none;
}

.stButton > button:hover {
    background: linear-gradient(
        90deg,
        #1D4ED8,
        #2563EB
    );
}

/* Prediction Card */
.result-box {
    background: white;
    padding: 25px;
    border-radius: 18px;
    border-left: 6px solid #2563EB;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.08);
}

/* Title */
.main-title {
    color: #1E3A5F;
    font-size: 42px;
    font-weight: 700;
    text-align: center;
}

/* Subtitle */
.sub-title {
    color: #64748B;
    text-align: center;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

[data-testid="stMetric"] label {
    color: #475569 !important;
}

[data-testid="stMetricValue"] {
    color: #0F172A !important;
}

[data-testid="stMetricLabel"] p {
    color: #475569 !important;
}

</style>
""", unsafe_allow_html=True)
# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🏥",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/predict"

# -------------------------
# Custom CSS
# -------------------------
st.markdown("""
<style>
.main-title {
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:#1f77b4;
}

.sub-title {
    text-align:center;
    color:gray;
    margin-bottom:30px;
}

.result-box {
    padding:20px;
    border-radius:15px;
    background-color:#f0f8ff;
    border:2px solid #1f77b4;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.markdown(
    '<p class="main-title">🏥 Insurance Premium Category Predictor</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">Predict insurance premium category using health and lifestyle information</p>',
    unsafe_allow_html=True
)

# -------------------------
# Sidebar
# -------------------------
st.sidebar.header("About")

st.sidebar.info(
    """
    This AI model predicts the insurance premium category
    based on customer demographics and health attributes.

    Categories:
    - Low
    - Medium
    - High
    """
)

# -------------------------
# Input Section
# -------------------------
col1, col2 = st.columns(2)

with col1:
    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=20.0,
        max_value=200.0,
        value=70.0
    )

    height = st.number_input(
        "Height (m)",
        min_value=1.0,
        max_value=2.5,
        value=1.70
    )

    income_lpa = st.number_input(
        "Annual Income (LPA)",
        min_value=1.0,
        value=10.0
    )

with col2:

    smoker = st.selectbox(
        "Smoker",
        ["No", "Yes"]
    )

    city = st.text_input(
        "City",
        value="Mumbai"
    )

    occupation = st.selectbox(
        "Occupation",
        [
            'private_job',
            'government_job',
            'business_owner',
            'freelancer',
            'student',
            'retired',
            'unemployed'
        ]
    )

# -------------------------
# BMI Calculation
# -------------------------
bmi = round(weight / (height ** 2), 2)

st.markdown("### Health Summary")

m1, m2, m3 = st.columns(3)

m1.metric("Age", age)
m2.metric("BMI", bmi)
m3.metric("Income (LPA)", income_lpa)

# -------------------------
# Prediction Button
# -------------------------
st.divider()

if st.button("🔮 Predict Premium Category", use_container_width=True):

    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker == "Yes",
        "city": city,
        "occupation": occupation
    }
    try:
        response = requests.post(API_URL, json=input_data)
        result = response.json()

        if response.status_code == 200 and "response" in result:
            prediction = result["response"]
            st.success(f"Predicted Insurance Premium Category: **{prediction['predicted_category']}**")
            st.write("🔍 Confidence:", prediction["confidence"])
            st.write("📊 Class Probabilities:")
            st.json(prediction["class_probabilities"])

        else:
            st.error(f"API Error: {response.status_code}")
            st.write(result)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")
#     try:
#         with st.spinner("Analyzing customer profile..."):

#             response = requests.post(
#                 API_URL,
#                 json=input_data,
#                 timeout=10
#             )

#         result = response.json()

#         if response.status_code == 200:

#             prediction = result["response"]

#             category = prediction["predicted_category"]
#             confidence = prediction["confidence"]

#             st.success("Prediction Completed")

#             st.markdown(
#                 f"""
#                 <div class="result-box">
#                 <h2>Predicted Category: {category}</h2>
#                 <h4>Confidence: {confidence:.2%}</h4>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )

#             # Probability Chart
#             probs = prediction["class_probabilities"]

#             df = pd.DataFrame(
#                 {
#                     "Category": probs.keys(),
#                     "Probability": probs.values()
#                 }
#             )

#             st.subheader("Class Probabilities")

#             st.bar_chart(
#                 df.set_index("Category")
#             )

#             st.subheader("Raw Output")
#             st.json(prediction)

#         else:
#             st.error(f"API Error: {response.status_code}")
#             st.json(result)

#     except requests.exceptions.ConnectionError:
#         st.error(
#             "❌ Unable to connect to FastAPI server. "
#             "Ensure the backend is running."
#         )

#     except Exception as e:
#         st.error(str(e))

# -------------------------
# Footer
# -------------------------
st.divider()

st.caption(
    "Built with FastAPI • Streamlit • Machine Learning"
)
# git add ml_model_api.py frontend_streamlit.py requirements.txt 