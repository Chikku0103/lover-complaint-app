import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Lover Complaint Hub ❤️", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: transparent;
    }
    html, body, .stApp {
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stButton>button {
        background-color: #ff69b4;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
    .stTextArea textarea {
        border-radius: 10px;
    }
    .complaint-box {
        background-color: rgba(255, 228, 225, 0.9);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; padding: 20px 0 10px 0;'>
        <img src='https://images.unsplash.com/photo-1583083527882-4bee9aba2eea?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTl8fGN1dGUlMjBjYXR8ZW58MHx8MHx8fDA%3D' width='80' style='border-radius: 50%; margin-right: 15px;'/>
        <img src='https://images.unsplash.com/photo-1533738363-b7f9aef128ce?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fGNhdHxlbnwwfHwwfHx8MA%3D%3D' width='80' style='border-radius: 50%;'/>
        <h1 style='color: #ff69b4; font-size: 50px; font-family: "Brush Script MT", cursive;'>Sree 💖 Chikku</h1>
        <p style='color: #8b0000; font-size: 20px;'>Together in love, even in complaints 😘</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; padding-top: 10px;'>
        <iframe width="300" height="170"
        src="https://www.youtube.com/embed/1-nnEM8chwo?rel=0&autoplay=0&loop=1&playlist=1-nnEM8chwo"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen></iframe>
        <p style='font-size: 14px; color: #ff69b4;'>I LOVE YOU SREEJANI 🥰🥰 - 🎶</p>
    </div>
""", unsafe_allow_html=True)


conn = sqlite3.connect('lover_complaints.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS complaints
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              complaint TEXT,
              status TEXT,
              complainer TEXT,
              timestamp TEXT)''')
conn.commit()

st.title("💌 Lover Complaint Page")
st.markdown("Welcome to the *Lover Complaint Hub*, where love meets honesty. Submit and resolve complaints with kindness! 💖")

account_holder = st.selectbox("Who's expressing feelings today? 😊", ["Sree", "Chikku"])
with st.form("complaint_form"):
    complaint = st.text_area("📝 Enter your heartfelt complaint here... But Ily Chengri ")
    submit_complaint = st.form_submit_button("❤️ Submit Complaint")

if submit_complaint:
    if complaint.strip() == "":
        st.error("Please write something before submitting!")
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO complaints (complaint, status, complainer, timestamp) VALUES (?, ?, ?, ?)",
                  (complaint, "Open", account_holder, timestamp))
        conn.commit()
        st.success("Your complaint has been safely submitted with love 💕")

st.subheader("📜 All Complaints")

c.execute("SELECT * FROM complaints ORDER BY id DESC")
complaints = c.fetchall()

if complaints:
    for complaint in complaints:
        with st.expander(f"💢 Complaint #{complaint[0]} by {complaint[3]} | Status: {complaint[2]}"):
            st.markdown(f"""
            <div class="complaint-box">
                <p><strong>🕒 Date:</strong> {complaint[4]}</p>
                <p><strong>💬 Complaint:</strong> {complaint[1]}</p>
            </div>
            """, unsafe_allow_html=True)

            if complaint[2] == "Open":
                if st.button(f"✅ Resolve Complaint #{complaint[0]}", key=complaint[0]):
                    c.execute("UPDATE complaints SET status = ? WHERE id = ?", ("Resolved", complaint[0]))
                    conn.commit()
                    st.success(f"Complaint #{complaint[0]} marked as resolved 💌")
                    st.rerun()
else:
    st.info("No complaints yet. Everything seems peaceful! ☮️")

import plotly.express as px

c.execute("SELECT complainer, COUNT(*) FROM complaints GROUP BY complainer")
data = c.fetchall()

if data:
    complainers = [row[0] for row in data]
    counts = [row[1] for row in data]
    
    fig = px.pie(
        names=complainers,
        values=counts,
        title="💔 Complaint Distribution Between Sree & Chikku",
        color_discrete_sequence=px.colors.sequential.RdPu
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig)

# --- Close DB ---
conn.close()
