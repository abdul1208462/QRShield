# 🛡️ QRShield

**AI-Powered Fake QR Code Detector**

QRShield is a Streamlit web app that scans QR codes and analyzes the URLs they contain for phishing and malicious indicators. Upload a QR image and QRShield decodes it, validates the link, calculates a risk score, and flags dangerous codes before you ever visit them.

The idea came from how common QR phishing has gotten — stickers slapped over restaurant menus, parking meters, fake payment codes. You scan it, it looks normal, and you're on a phishing page. QRShield decodes the code and runs some checks on the URL so you can catch the obvious red flags first.

## 🔗 Live Demo

https://qrshield-4appdljywhquiciuwraralh.streamlit.app/

## Features

- **QR Code Scanner** — decodes QR images (PNG, JPG, JPEG) using OpenCV
- **URL Validation** — confirms the decoded data is a real URL
- **Threat Analysis** — checks for HTTP-over-HTTPS, raw IP addresses, URL shorteners, and suspicious keywords (login, bank, verify, password, etc.)
- **Risk Score** — a 0–100 score with Low / Medium / High threat levels
- **Scan History** — logs every scan to a CSV you can download
- **Clean dark UI** — custom-styled Streamlit interface

## Prerequisites

Python 3.10+

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/QRShield.git
cd QRShield
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

Then open the local URL Streamlit prints (usually http://localhost:8501).

## Tech Stack

| Component      | Library          |
|----------------|------------------|
| Web UI         | Streamlit        |
| QR decoding    | OpenCV           |
| Image handling | Pillow, NumPy    |
| URL validation | validators       |
| Data / history | pandas           |
| PDF reporting  | reportlab        |

## How the Risk Score Works

| Indicator                   | Points   |
|-----------------------------|----------|
| Uses HTTP instead of HTTPS  | +25      |
| Contains a raw IP address   | +30      |
| Suspicious keyword          | +10 each |
| URL shortener               | +20      |

| Score  | Threat Level  |
|--------|---------------|
| < 25   | 🟢 Low / Safe |
| 25–59  | 🟡 Medium     |
| ≥ 60   | 🔴 High       |

## Project Structure

QRShield/
├── app.py # Main Streamlit application
├── requirements.txt # Python dependencies
├── scan_history.csv # Auto-generated scan log (gitignored)

## A Note

This is a project I built to learn and to raise awareness about QR phishing — it uses basic rule-based checks, not a real security engine. It's an educational / awareness tool, not a guaranteed security scanner. Always use your own judgment before opening a link or entering personal information.
└── README.md

## Project Structure
