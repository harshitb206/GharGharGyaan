import streamlit as st
import requests
from gtts import gTTS
from twilio.rest import Client
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
import os
import threading

# ---------------------- Twilio Setup ----------------------
TWILIO_ACCOUNT_SID = "ACdf84b135b29e84b7d8864cf63e2ecd95"
TWILIO_AUTH_TOKEN = "8bf3e7a33964a279358c0d5e7c39390f"
TWILIO_PHONE_NUMBER = "+15392810268"

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ---------------------- Flask + API ----------------------
flask_app = Flask(__name__)

@flask_app.route("/sms", methods=["POST"])
def sms_reply():
    number = request.form.get("From")
    message_body = request.form.get("Body")
    resp = MessagingResponse()
    resp.message(f"Hello {number}, you said: {message_body}")
    return str(resp)

@flask_app.route("/voice", methods=["POST"])
def voice_reply():
    response = VoiceResponse()
    response.say("Namaste. Welcome to Ghar Ghar Gyaan.", voice="Polly.Emma")
    response.pause(length=1)
    response.say("Please wait while we connect you to important information.", voice="Polly.Emma")
    response.record(timeout=10, transcribe=True)
    response.hangup()
    return str(response)

@flask_app.route("/call", methods=["POST"])
def make_call():
    to_number = request.form.get("To")
    try:
        call = twilio_client.calls.create(
            to=to_number,
            from_=TWILIO_PHONE_NUMBER,
            url="http://demo.twilio.com/docs/voice.xml"
        )
        return f"Call initiated! Call SID: {call.sid}"
    except Exception as e:
        return f"Error initiating call: {e}"

def run_flask():
    flask_app.run(port=5001)

threading.Thread(target=run_flask, daemon=True).start()

# ---------------------- Streamlit UI ----------------------
st.set_page_config(page_title="GharGharGyaan", layout="wide")

st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            background-color: #FAF8F0;
            color: #333333;
        }

        .stButton > button {
            background-color: #FF6B81;
            color: white;
            border-radius: 12px;
            padding: 0.6em 1.2em;
            font-size: 16px;
            font-weight: bold;
            border: none;
        }

        .stButton > button:hover {
            background-color: #FF4E70;
        }

        .stTextInput > div > input,
        .stTextArea > div > textarea,
        .stSelectbox > div > div {
            background-color: #FFF8FC;
            border: 1px solid #DDC9E9;
            border-radius: 10px;
            padding: 0.5em;
        }

        .block-container {
            padding: 2rem 3rem;
        }

        audio {
            margin-top: 10px;
        }

        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #4B0082;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.image("https://i.imgur.com/6M513yc.png", use_column_width=True)
st.sidebar.title("GharGharGyaan")
st.sidebar.markdown("**Empowering Rural Women with Legal & Health Rights** 🌼")

option = st.sidebar.radio(
    "Select an option:",
    ("Eligibility Checker", "Know Your Rights", "Stories", "Legal Document Generator", "SMS Alerts", "Call Feature")
)

API_URL = "http://localhost:5000/api"

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    os.makedirs("audio", exist_ok=True)
    filename = "audio/output.mp3"
    tts.save(filename)
    return filename

def send_sms(to, message):
    try:
        msg = twilio_client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to
        )
        return f"Message sent! SID: {msg.sid}"
    except Exception as e:
        return f"Error sending SMS: {e}"

# ---------------------- Streamlit Routes ----------------------

# 1. Eligibility Checker
if option == "Eligibility Checker":
    st.header("🧾 Eligibility Checker")
    answers = {
        "pregnant": st.checkbox("Are you pregnant?"),
        "aadhar": st.checkbox("Do you have an Aadhar card?"),
        "widow": st.checkbox("Are you a widow?"),
        "disabled": st.checkbox("Do you have a disability?"),
        "low_income": st.checkbox("Are you from a low-income background?")
    }

    if st.button("✅ Check Eligibility"):
        res = requests.post(f"{API_URL}/eligibility", json=answers).json()
        st.subheader("Eligibility Result:")

        message_text = "You are eligible for:\n"

        if res["eligibleSchemes"]:
            with st.container():
                for scheme in res["eligibleSchemes"]:
                    info = f"{scheme['name']}: {scheme['benefits']}"
                    st.success(f"✅ {info}")
                    message_text += "- " + info + "\n"
        else:
            st.warning("❌ No schemes available based on your answers.")

        st.session_state["eligibility_message"] = message_text

# 2. Know Your Rights
elif option == "Know Your Rights":
    st.header("📚 Know Your Rights")
    category = st.selectbox("Select category", ["maternity", "domestic_violence", "immunization", "pensions", "legal_aid"])
    if st.button("🔍 Get Info"):
        res = requests.get(f"{API_URL}/rights/{category}").json()
        with st.expander("Click to hear your rights"):
            st.text(res["info"])
            audio_path = text_to_speech(res["info"])
            st.audio(audio_path)

# 3. Stories
elif option == "Stories":
    st.header("📖 Real-Life Stories")
    if st.button("🎧 Hear Stories"):
        res = requests.get(f"{API_URL}/stories").json()
        for story in res:
            with st.expander(story["name"]):
                st.markdown(story["story"])
                audio_path = text_to_speech(story["story"])
                st.audio(audio_path)

# 4. Legal Document Generator
elif option == "Legal Document Generator":
    st.header("📄 Legal Document Generator")
    name = st.text_input("Your Name")
    scheme = st.text_input("Scheme Name")
    if st.button("🛠️ Generate Document"):
        res = requests.post(f"{API_URL}/documents", json={"name": name, "scheme": scheme}).json()
        st.text_area("📜 Your Document", value=res["document"], height=200)

# 5. SMS Alerts
elif option == "SMS Alerts":
    st.header("📩 SMS Alerts")
    recipient = st.text_input("📱 Enter recipient phone number (e.g., +91xxxxxxxxxx)")
    if st.button("📤 Send Eligibility Result via SMS"):
        if "eligibility_message" in st.session_state:
            result = send_sms(recipient, st.session_state["eligibility_message"])
            st.success(result)
        else:
            st.warning("❗ Please check eligibility first before sending SMS.")

# 6. Call Feature
elif option == "Call Feature":
    st.header("📞 Call Feature")
    phone_number = st.text_input("📱 Enter phone number to call", value="+91")
    if st.button("📲 Call This Number"):
        try:
            response = requests.post("http://localhost:5001/call", data={"To": phone_number})
            st.success(f"📞 Call initiated! {response.text}")
        except Exception as e:
            st.error(f" Error initiating the call: {e}")
