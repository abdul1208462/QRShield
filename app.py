import streamlit as st
import cv2
import numpy as np
from PIL import Image
import validators
import re
import pandas as pd
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

st.set_page_config(
    page_title="QRShield",
    page_icon="🛡",
    layout="wide"
)
st.markdown("""
<style>

.main{
background:#0f172a;
}

.block-container{
padding-top:2rem;
}

.stButton>button{
background:#00c853;
color:white;
border-radius:12px;
height:50px;
width:100%;
font-size:18px;
font-weight:bold;
transition:0.3s;
}

.stButton>button:hover{
background:#00e676;
transform:scale(1.03);
}

[data-testid="stMetric"]{
background:#1e293b;
padding:15px;
border-radius:15px;
box-shadow:0px 0px 15px rgba(0,255,170,.2);
}

.stAlert{
border-radius:15px;
}

</style>
""", unsafe_allow_html=True)
HISTORY_FILE = "scan_history.csv"

if not os.path.exists(HISTORY_FILE):
    df = pd.DataFrame(columns=[
        "Date",
        "URL",
        "Risk Score",
        "Status"
    ])
    df.to_csv(HISTORY_FILE, index=False)
st.markdown("""
<style>

.stApp{
background:#0f172a;
color:white;
}

h1{
text-align:center;
color:#38bdf8;
}

.card{
background:#1e293b;
padding:20px;
border-radius:15px;
margin-top:20px;
box-shadow:0px 0px 12px rgba(0,255,255,.2);
}

.result{
font-size:22px;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align:center;color:#00e676;'>
🛡 QRShield
</h1>

<h4 style='text-align:center;color:white;'>
AI Powered Fake QR Code Detector
</h4>
""", unsafe_allow_html=True)
st.write("### Fake QR Code Detector")
if "total_scans" not in st.session_state:
    st.session_state.total_scans = 0

if "dangerous_scans" not in st.session_state:
    st.session_state.dangerous_scans = 0

col1, col2 = st.columns(2)

with col1:
    st.metric("📄 Total Scans", st.session_state.total_scans)

with col2:
    st.metric("🚨 Dangerous", st.session_state.dangerous_scans)

    
with st.sidebar:

    st.title("🛡 QRShield")

    st.markdown("---")

    st.info(
        "Upload a QR code to check if it is safe or potentially malicious."
    )

    st.markdown("### Features")
    st.write("✅ QR Code Scanner")
    st.write("✅ URL Validation")
    st.write("✅ Threat Analysis")
    st.write("✅ Risk Score")
    st.write("✅ PDF Report")
    st.write("✅ Scan History")

    st.markdown("---")
    st.caption("Version 1.0")
uploaded = st.file_uploader(
    "Upload QR Code",
    type=["png","jpg","jpeg"]
)

if uploaded:

    image = Image.open(uploaded)

    st.image(image, width=300)

    image_np = np.array(image)

    detector = cv2.QRCodeDetector()

    qr_data, points, _ = detector.detectAndDecode(image_np)

    if qr_data:
        st.success("✅ QR Code Detected")
    else:
        st.error("❌ No QR Code Found")
        st.stop()

    st.markdown('<div class="card">',unsafe_allow_html=True)

    st.subheader("Decoded Data")

    st.code(qr_data)

    st.markdown("</div>",unsafe_allow_html=True)

    if validators.url(qr_data):

            st.success("Valid URL Detected")

            score=0

            reasons=[]

            if not qr_data.startswith("https://"):
                score+=25
                reasons.append("Uses HTTP instead of HTTPS")

            if re.search(r"\d+\.\d+\.\d+\.\d+",qr_data):
                score+=30
                reasons.append("Contains IP Address")

            suspicious=[
                "login",
                "verify",
                "bank",
                "gift",
                "free",
                "wallet",
                "password"
            ]

            for word in suspicious:
                if word in qr_data.lower():
                    score+=10
                    reasons.append(f"Contains '{word}'")

            shorteners=[
                "bit.ly",
                "tinyurl",
                "t.co",
                "is.gd"
            ]

            for s in shorteners:
                if s in qr_data:
                    score+=20
                    reasons.append("URL Shortener Used")

            st.subheader("Risk Score")

        
            st.progress(score / 100)
            st.metric(
    "Overall Risk",
    f"{score}/100"
)

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Risk Score", f"{score}/100")

            with col2:
                if score < 25:
                    st.metric("Threat Level", "🟢 Low")
                elif score < 60:
                    st.metric("Threat Level", "🟡 Medium")
                else:
                    st.metric("Threat Level", "🔴 High")

            if score < 25:
             status = "SAFE"
             st.success("🟢 SAFE")

            elif score < 60:
              status = "WARNING"
              st.warning("🟡 WARNING")

            else:
             status = "DANGEROUS"
             st.error("🔴 DANGEROUS")

            new_scan = pd.DataFrame([{
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "URL": qr_data,
            "Risk Score": score,
            "Status": status
}])

            history = pd.read_csv(HISTORY_FILE)
            history = pd.concat([history, new_scan], ignore_index=True)
            history.to_csv(HISTORY_FILE, index=False)
            st.session_state.total_scans += 1

            if status == "DANGEROUS":
                st.session_state.dangerous_scans += 1

            st.subheader("Threat Analysis")

            with st.expander("🔍 View Threat Details"):

                if reasons:
                    for r in reasons:
                        st.error(r)
                else:
                    st.success("✅ No suspicious indicators detected.")

                st.subheader("🛡 Recommendation")

                if score < 25:
                    st.success(
                        "This QR code appears safe. No major phishing indicators were detected."
                    )
                elif score < 60:
                    st.warning(
                        "Be careful. Verify the website before entering any personal information."
                    )
                else:
                    st.error(
                        "High-risk QR code detected. Do not enter passwords, OTPs, or banking details."
                    )

    else:
        st.error("❌ QR code does not contain a valid URL.")
                

st.subheader("📜 Scan History")

history = pd.read_csv(HISTORY_FILE)

st.dataframe(history.tail(10), use_container_width=True)
with open(HISTORY_FILE, "rb") as file:

    st.download_button(
        label="⬇ Download Scan History",
        data=file,
        file_name="scan_history.csv",
        mime="text/csv"
    )