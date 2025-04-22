import streamlit as st
import requests
from gtts import gTTS
from twilio.rest import Client
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
import os
import threading

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

//twilio is secret
[twilio]
account_sid = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
auth_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
phone_number = "+1xxxxxxxxxx"


twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ---------------------- API + TTS ----------------------
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
    custom_msg = request.args.get("msg", "Namaste! Welcome to Ghar Ghar Gyaan.")

    response = VoiceResponse()
    response.say(custom_msg, voice="Polly.Aditi", language="hi-IN")
    response.hangup()

    return str(response)

def run_flask():
    flask_app.run(port=5000)

threading.Thread(target=run_flask, daemon=True).start()

@flask_app.route("/call", methods=["POST"])
def make_call():
    to_number = request.form.get("To")
    from_number = TWILIO_PHONE_NUMBER

    try:
        call = twilio_client.calls.create(
            to=to_number,
            from_=from_number,
            url="http://demo.twilio.com/docs/voice.xml"
        )
        return f"Call initiated! Call SID: {call.sid}"
    except Exception as e:
        return f"Error initiating call: {e}"
# ------------------ Streamlit UI ------------------

# Custom CSS to style the page
st.markdown("""
    <style>
        body {
            background-color: #E0F7FA;  /* Light teal background */
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
        }

        .stButton>button {
            background-color: #00796B;  /* Deep teal for buttons */
            color: white !important;
            border-radius: 12px;
            padding: 12px 30px;
            font-size: 16px;
            border: none;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            transition: background-color 0.3s ease, transform 0.2s ease;
        }

        .stButton>button:hover {
            background-color: #004D40 !important;  /* Darker teal on hover */
            color: white !important;
            transform: scale(1.05);
        }

        .stSelectbox>div, .stTextInput>div, .stCheckbox>div, .stTextArea>div {
            background-color: #FFFFFF;  /* White background for input areas */
            border-radius: 10px;
            padding: 2px;
            box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.1);
        }

        .stTextInput>input, .stTextArea>textarea {
            border: 1px solid #00796B;
            border-radius: 8px;
            padding: 8px;
            font-size: 14px;
            color: #00796B;
        }

        .stTextInput>input:focus, .stTextArea>textarea:focus {
            border-color: #004D40;  /* Dark teal border on focus */
        }

        .stTitle, .stHeader {
            color: #004D40;  /* Dark teal for headings */
            font-family: 'Verdana', sans-serif;
            font-weight: bold;
            text-align: center;
        }

        .stText, .stMarkdown {
            color: #00796B;  /* Lighter teal for regular text */
            font-size: 16px;
        }

        .stRadio, .stSelectbox {
            margin-top: 10px;
        }

        .stAlert {
            background-color: #2F4F4F;
            color: #212121;
            font-weight: bold;
            padding: 10px;
            border-radius: 8px;
        }

        .stSidebar {
            background-color: #00796B;
            color: white;
        }

        .stSidebar .stRadio>div {
            background-color: #004D40;
            border-radius: 8px;
            padding: 10px;
        }

        .stSidebar .stRadio>div:hover {
            background-color: #00332A;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("Ghar Ghar Gyaan")
# Sidebar navigation menu
option = st.sidebar.radio(
    "Select an option:",
    ("Eligibility Checker", "Know Your Rights", "Stories", "Legal Document Generator", "SMS Alerts", "Call Feature", "Student Scholarships")
)

# 5. Student Scholarships
if option == "Student Scholarships":
    st.markdown("<h2 style='color:#004D40;text-align:center;'>🎓 Student Scholarships</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00796B;'>Please answer the following to find scholarships you may be eligible for:</p>", unsafe_allow_html=True)

    # 🧾 Identity & Income
    with st.expander("📄 Personal & Financial Information"):
        is_student = st.checkbox("📚 Are you currently a school or college student?", key="is_student")
        low_income = st.checkbox("💸 Is your family income below ₹2 lakh/year?", key="student_low_income")
        orphan = st.checkbox("🧒 Are you an orphan or without parental support?", key="student_orphan")

    # 🌍 Location & Community
    with st.expander("🌍 Location & Community"):
        rural_area = st.checkbox("🏡 Do you live in a rural or backward area?", key="rural_area")
        minority = st.checkbox("🙏 Are you from a minority community (SC/ST/OBC/Muslim/Christian)?", key="minority")

    if st.button("🔍 Find Scholarships"):
        scholarships = []

        if is_student and low_income:
            scholarships.append({
                "name": "🎓 NSP Pre-Matric Scholarship",
                "benefits": "Up to ₹10,000 per year for school students from low-income families."
            })

        if is_student and low_income and minority:
            scholarships.append({
                "name": "🕌 Minority Scholarship Scheme",
                "benefits": "₹5,000 to ₹25,000 per year for students from minority communities."
            })

        if is_student and rural_area:
            scholarships.append({
                "name": "🏫 PM YASASVI Scholarship",
                "benefits": "Support for OBC/EBC/DNT students in classes 9 to 12."
            })

        if is_student and orphan:
            scholarships.append({
                "name": "👶 Foster Child Education Scheme",
                "benefits": "Free education + stipend for orphans under state schemes."
            })

        if scholarships:
            st.markdown("### 📋 Eligible Scholarships:")
            message = ""
            for s in scholarships:
                st.markdown(f"""
                    <div style='background-color:#F0FFFF;padding:12px;border-left:5px solid #00796B;margin-bottom:10px;border-radius:8px;'>
                        <strong style='color:#004D40'>{s['name']}</strong><br/>
                        <span style='color:#555'>{s['benefits']}</span>
                    </div>
                """, unsafe_allow_html=True)
                message += f"{s['name']}: {s['benefits']}\n"

            # 🎧 Optional TTS Audio
            # Ensure text_to_speech function is defined before calling it
            def text_to_speech(text):
                tts = gTTS(text=text, lang='en')
                os.makedirs("audio", exist_ok=True)
                filename = "audio/output.mp3"
                tts.save(filename)
                return filename

            audio_path = text_to_speech(message)
            st.audio(audio_path)

        else:
            st.warning("😔 No scholarships matched your responses. Try modifying your answers.")



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

if option == "Eligibility Checker":
    st.header("1. Eligibility Checker")
    st.write("Please answer the following questions to check your eligibility:")

    # 🪪 Identity Related
    with st.expander("🪪 Identity Related"):
        aadhar = st.checkbox("Do you have an Aadhar card?", key="aadhar")
        voter_id = st.checkbox("Do you have a Voter ID?", key="voter_id")
        ration_card = st.checkbox("Do you have a valid Ration Card?", key="ration_card")
        bpl_card = st.checkbox("Do you have a BPL (Below Poverty Line) card?", key="bpl_card")
        caste_certificate = st.checkbox("Do you have a caste certificate (SC/ST/OBC)?", key="caste_certificate")

    # 🧑‍⚖️ Social Status
    with st.expander("🧑‍⚖️ Social Status"):
        widow = st.checkbox("Are you a widow?", key="widow")
        single_mother = st.checkbox("Are you a single mother?", key="single_mother")
        orphan = st.checkbox("Are you an orphan or without family support?", key="orphan")
        elderly = st.checkbox("Are you a senior citizen (60+)?", key="elderly")
        female_headed = st.checkbox("Is your household female-headed?", key="female_headed")

    # 💸 Financial Background
    with st.expander("💸 Financial Background"):
        low_income = st.checkbox("Is your monthly family income below ₹10,000?", key="low_income")
        jobless = st.checkbox("Is the primary earner currently unemployed?", key="jobless")
        landless = st.checkbox("Do you not own any agricultural land?", key="landless")
        daily_wage = st.checkbox("Do you depend on daily wage labor?", key="daily_wage")
        debt = st.checkbox("Is your family under any financial debt?", key="debt")
        no_bank_account = st.checkbox("Do you lack access to a bank account?", key="no_bank_account")

    # ♿ Health Related
    with st.expander("♿ Health Related"):
        disabled = st.checkbox("Do you have any form of disability?", key="disabled")
        chronic_disease = st.checkbox("Do you suffer from a chronic illness (like TB, HIV)?", key="chronic_disease")
        mental_health = st.checkbox("Do you have a diagnosed mental health condition?", key="mental_health")
        maternal_health = st.checkbox("Are you pregnant or lactating?", key="maternal_health")
        child_with_disability = st.checkbox("Do you have a child with special needs?", key="child_with_disability")

    # Collect all answers
    answers = {
        "aadhar": aadhar,
        "voter_id": voter_id,
        "ration_card": ration_card,
        "bpl_card": bpl_card,
        "caste_certificate": caste_certificate,
        "widow": widow,
        "single_mother": single_mother,
        "orphan": orphan,
        "elderly": elderly,
        "female_headed": female_headed,
        "low_income": low_income,
        "jobless": jobless,
        "landless": landless,
        "daily_wage": daily_wage,
        "debt": debt,
        "no_bank_account": no_bank_account,
        "disabled": disabled,
        "chronic_disease": chronic_disease,
        "mental_health": mental_health,
        "maternal_health": maternal_health,
        "child_with_disability": child_with_disability
    }

    if st.button("Check Eligibility"):
        try:
            res = requests.post(f"{API_URL}/eligibility", json=answers).json()
            st.subheader("Eligibility Result:")

            message_text = "You are eligible for:\n"

            if res["eligibleSchemes"]:
                for scheme in res["eligibleSchemes"]:
                    info = f"- {scheme['name']}: {scheme['benefits']}"
                    st.text(info)
                    message_text += info + "\n"
            else:
                st.text("❌ No schemes available based on your answers.")

            st.session_state["eligibility_message"] = message_text

        except Exception as e:
            st.error("⚠️ Error while checking eligibility.")
            st.exception(e)

# 2. Know Your Rights
elif option == "Know Your Rights":
    st.header("2. Know Your Rights")
    category = st.selectbox("Select category", ["maternity", "domestic violence", "immunization", "pension", "legal aid","scholarships"])
    if st.button("Get Info"):
        res = requests.get(f"{API_URL}/rights/{category}").json()
        st.text(res["info"])
        audio_path = text_to_speech(res["info"])
        st.audio(audio_path)

# 3. Stories
elif option == "Stories":
    st.header("3. Stories")
    if st.button("Hear Stories"):
        res = requests.get(f"{API_URL}/stories").json()
        for story in res:
            st.markdown(f"{story['name']}: {story['story']}")
            audio_path = text_to_speech(story["story"])
            st.audio(audio_path)

# 4. Legal Document Generator
elif option == "Legal Document Generator":
    st.header("4. Legal Document Generator")
    name = st.text_input("Your Name")
    scheme = st.text_input("Scheme Name")
    if st.button("Generate Document"):
        res = requests.post(f"{API_URL}/documents", json={"name": name, "scheme": scheme}).json()
        st.text_area("Your Document", value=res["document"], height=200)

# 5. SMS Alerts
elif option == "SMS Alerts":
    st.header("5. SMS Alerts")
    recipient = st.text_input("Enter recipient phone number (e.g., +91xxxxxxxxxx)")
    if st.button("Send Eligibility Result via SMS"):
        if "eligibility_message" in st.session_state:
            result = send_sms(recipient, st.session_state["eligibility_message"])
            st.success(result)
        else:
            st.warning("Please check eligibility first before sending SMS.")

# 6. Call Feature
elif option == "Call Feature":
    st.header("6. Contact Us ")

    if st.button("Click to Call"):
        phone_number = "+91*********"  # Your phone number for the call (you can make this dynamic if needed)

        try:
            response = requests.post("http://localhost:5000/call", data={"To": phone_number})
            st.success(f"Call initiated! {response.text}")
        except Exception as e:
            st.error(f"Error initiating the call: {e}")
# 5. Student Scholarships
elif option == "Student Scholarships":
    st.header("🎓 Scholarships for Students")
    st.write("Answer a few questions to check for available scholarships:")

    # Simple scholarship eligibility inputs
    is_student_scholarship = st.checkbox("📚 Are you currently a school or college student?", key="iss_student_scholarship")
    low_income_scholarship = st.checkbox("💸 Is your family income below ₹2 lakh/year?", key="student_low_income_scholarship")
    orphan_scholarship = st.checkbox("🧒 Are you an orphan or without parental support?", key="student_orphan_scholarship")
    rural_area_scholarship = st.checkbox("Do you reside in a rural/backward area?", key="rural_area_scholarship")
    minority_scholarship = st.checkbox("Do you belong to a minority community (SC/ST/OBC/Muslim/Christian)?", key="minority_scholarship ")

    if st.button("Show Scholarships"):
        # Sample hardcoded scholarships — in production, fetch from an API or DB
        scholarships = []

        if is_student_scholarship and low_income_scholarship:
            scholarships.append({
                "name": "NSP Pre-Matric Scholarship",
                "benefits": "Up to ₹10,000 per year for school students from low-income families"
            })

        if is_student_scholarship and low_income_scholarship and minority_scholarship:
            scholarships.append({
                "name": "Minority Scholarship Scheme",
                "benefits": "₹5,000 to ₹25,000 per year for students from minority communities"
            })

        if is_student_scholarship and rural_area_scholarship:
            scholarships.append({
                "name": "PM YASASVI Scholarship",
                "benefits": "Scholarship for OBC/EBC/DNT students studying in Class 9 to 12"
            })

        if is_student_scholarship and orphan_scholarship:
            scholarships.append({
                "name": "State Government Foster Child Education Scheme",
                "benefits": "Free education and monthly stipend for orphan students"
            })

        if scholarships:
            st.subheader("📚 Available Scholarships:")
            message = ""
            for s in scholarships:
                info = f"- **{s['name']}**: {s['benefits']}"
                st.markdown(info)
                message += f"{s['name']}: {s['benefits']}\n"
            audio_path = text_to_speech(message)
            st.audio(audio_path)
        else:
            st.warning("❌ No scholarships match the selected criteria.")
