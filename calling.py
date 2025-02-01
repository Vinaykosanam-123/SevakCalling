import os
import sqlite3
import streamlit as st
import pandas as pd
from twilio.rest import Client

# Set up SQLite database
def init_db():
    conn = sqlite3.connect("calling_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            call_sid TEXT,
            to_number TEXT,
            from_number TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

# Function to store call details
def store_call(call_sid, to_number, from_number, status):
    conn = sqlite3.connect("calling_database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO calls (call_sid, to_number, from_number, status) VALUES (?, ?, ?, ?)",
                   (call_sid, to_number, from_number, status))
    conn.commit()
    conn.close()

# Function to retrieve call history
def get_call_history():
    conn = sqlite3.connect("calling_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM calls ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Initialize the database
init_db()

# Streamlit UI
st.title("Twilio Call Automation")

from_number = "+18482836037"
to_number = st.text_input("Enter recipient's phone number:")
audio_url = "https://flavescent-serval-2251.twil.io/assets/sevak_audio%20(online-audio-converter.com).mp3"

if st.button("Make Call") and to_number:
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        client = Client(account_sid, auth_token)

        call = client.calls.create(
            from_=from_number,
            to=to_number,
            url=audio_url,
        )

        st.success(f"Call placed successfully! Call SID: {call.sid}")
        store_call(call.sid, to_number, from_number, "registration completed")
    except Exception as e:
        st.error(f"Error: {e}")

st.subheader("Calling Database")
call_history = get_call_history()

if call_history:
    df = pd.DataFrame(call_history, columns=["ID", "Call SID", "To", "From", "Status"])
    st.dataframe(df)
else:
    st.write("No calling database available.")
