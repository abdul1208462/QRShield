import streamlit as st
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import validators
import re

st.set_page_config(
    page_title="QRShield",
    page_icon="🛡",
    layout="wide"
)

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

st.title("🛡 QRShield")
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

uploaded = st.file_uploader(
    "Upload QR Code",
    type=["png","jpg","jpeg"]
)

if uploaded:

    image = Image.open(uploaded)

    st.image(image,width=300)

    img=np.array(image)

    decoded=decode(img)

    if decoded:
        st.session_state.total_scans += 1

        qr_data=decoded[0].data.decode()

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

            # Summary badge and dangerous count
            if score < 25:
                st.success("SAFE")
            elif score < 60:
                st.warning("WARNING")
            else:
                st.error("DANGEROUS")
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

            if reasons:
                for r in reasons:
                    st.error(r)
            else:
                st.write("✅ No suspicious indicators found.")

        else:

            st.error("QR code does not contain a valid URL.")

    else:

        st.error("No QR code detected.")