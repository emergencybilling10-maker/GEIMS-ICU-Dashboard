import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json

# Page Config
st.set_page_config(page_title="GEIMS ICU Management", layout="wide")

# --- 1. SECURE DATABASE CONNECTION ---
if "textkey" in st.secrets:
    try:
        key_dict = json.loads(st.secrets["textkey"])
        creds = service_account.Credentials.from_service_account_info(key_dict)
        db = firestore.Client(credentials=creds)
    except Exception as e:
        st.error(f"Database Secret Error: {e}")
        st.stop()
else:
    st.warning("Admin: Please add the Firestore JSON key to Streamlit Secrets.")
    st.stop()

# --- 2. FULL ICU & HDU DATA ---
icu_structure = {
    "8th Floor - RICU / MICU / SICU": [
        "B-ICU-20", "B-ICU-17", "B-ICU-18", "MICU-1", "MICU-2", "MICU-3", "MICU-4", "MICU-5", 
        "SICU-1", "SICU-2", "SICU-3", "SICU-4", "SICU-5", "RICU-1", "RICU-2", "RICU-3", 
        "RICU-4", "RICU-5", "B-ICU-31", "B-ICU-27"
    ],
    "8th Floor - Respiratory ICU": [
        "ICU-8F-1", "ICU-8F-2", "ICU-8F-3", "ICU-8F-4", "ICU-8F-5", "ICU-8F-6", 
        "ICU-8F-7", "ICU-8F-8", "ICU-8F-9", "ICU-8F-10"
    ],
    "8th Floor - Neuro SICU & HDU": [
        "N-SICU-1", "N-SICU-2", "N-SICU-3", "N-SICU-4", "N-SICU-5", "N-SICU-6",
        "N-SICU-7", "N-SICU-8", "N-SICU-9", "N-SICU-10", "N-SICU-11", "N-SICU-12",
        "N-SICU-13", "N-SICU-14", "N-SICU-15",
        "GF-Neuro-HDU-1", "GF-Neuro-HDU-2", "GF-Neuro-HDU-3", "GF-Neuro-HDU-4", 
        "GF-Neuro-HDU-5", "GF-Neuro-HDU-6", "GF-Neuro-HDU-7", "GF-Neuro-HDU-8",
        "GF-Neuro-HDU-9", "GF-Neuro-HDU-10", "GF-Neuro-HDU-11", "GF-Neuro-HDU-12",
        "GF-Neuro-HDU-16", "GF-Neuro-HDU-14", "GF-Neuro-HDU-15"
    ],
    "6th Floor - Ayushman ICU (PMJAY)": [
        "PMJAY-1", "PMJAY-2", "PMJAY-3", "PMJAY-4", "PMJAY-5", "PMJAY-6", "PMJAY-7", "PMJAY-8", 
        "ICU-9", "PMJAY-9", "PMJAY-10", "PMJAY-11", "PMJAY-12", "PMJAY-13", "PMJAY-14", 
        "PMJAY-15", "PMJAY-16", "PMJAY-17", "PMJAY-18", "PMJAY-19", "PMJAY-20", "PMJAY-21", 
        "PMJAY-22", "PMJAY-23", "PMJAY-24"
    ],
    "4th Floor - CCU / CTVS / SICU 2": [
        "ccu-121", "B-CCU-1", "B-CCU-2", "B-CCU-3", "B-CCU-4", "B-CCU-5", "B-CCU-6", "B-CCU-7", 
        "B-CCU-8", "B-CCU-9", "B-CCU-10", "B-CCU-11", "B-CCU-12", "B-CCU-16", "B-CCU-14", "B-CCU-15",
        "CTVS-1", "CTVS-2", "CTVS-3", "CTVS-4", "CTVS-5", "CTVS-6", "CTVS-7", "CTVS-8", "CTVS-9", "CTVS-10",
        "CCU-2-1", "CCU-2-2", "CCU-2-3", "CCU-2-4", "CCU-2-5", "CCU-2-6", "CCU-2-7", "CCU-2-8", "CCU-2-9", "CCU-2-10",
        "SICU-2-1", "SICU-2-2", "SICU-2-3", "SICU-2-4", "SICU-2-5", "SICU-2-6", "SICU-2-7", "SICU-2-8",
        "Burn-ICU-1", "Burn-ICU-2"
    ],
    "3rd Floor - PICU": [
        "PICU-1", "PICU-2", "PICU-3", "PICU-4", "PICU-5", "PICU-6", "PICU-7"
    ]
}

# --- 3. ADMIN PANEL ---
with st.sidebar:
    st.header("🔐 ICU Master Control")
    pwd = st.text_input("Enter Admin Password", type="password")
    is_admin = (pwd == "Geims248001")
    
    if is_admin:
        st.success("Access Granted")
        all_beds = [b for w in icu_structure.values() for b in w]
        sel_bed = st.selectbox("Select ICU Bed", sorted(all_beds))
        # Updated statuses: Added SHIFTING and BOOKED
        new_stat = st.selectbox("Status", ["VACANT", "OCCUPIED", "BOOKED", "SHIFTING", "VENTILATOR ON", "CRITICAL", "TO DISCHARGE", "MAINTENANCE"])
        p_name = st.text_input("Patient Name (leave blank to clear)")
        
        if st.button("Update ICU Record"):
            db.collection("icu_beds").document(sel_bed).set({
                "status": new_stat, 
                "patient": p_name
            })
            st.success(f"Updated {sel_bed}")
            st.rerun()
    else:
        st.info("View-Only Mode")

# --- 4. DASHBOARD DISPLAY ---
docs = db.collection("icu_beds").stream()
live_data = {doc.id: doc.to_dict() for doc in docs}

# Colors matching your previous professional layout
status_colors = {
    "VACANT": "#FFFFFF", "OCCUPIED": "#000000", "BOOKED": "#90EE90", 
    "SHIFTING": "#FFA500", "VENTILATOR ON": "#1E90FF", "CRITICAL": "#B22222", 
    "TO DISCHARGE": "#ADD8E6", "MAINTENANCE": "#E0E0E0"
}

st.title("🚑 GEIMS ICU & Specialized Units Live Status")
for unit, beds in icu_structure.items():
    st.subheader(unit)
    cols = st.columns(5)
    for i, bed in enumerate(beds):
        data = live_data.get(bed, {"status": "VACANT", "patient": ""})
        bg = status_colors.get(data['status'], "#FFFFFF")
        txt = "white" if data['status'] in ["OCCUPIED", "CRITICAL", "VENTILATOR ON"] else "black"
        
        with cols[i % 5]:
            st.markdown(f"""
                <div style="background-color:{bg}; color:{txt}; padding:10px; border:2px solid #444; border-radius:8px; text-align:center; height:110px; margin-bottom:15px;">
                    <div style="font-size:12px; font-weight:bold;">{bed}</div>
                    <div style="font-size:10px;">{data['status']}</div>
                    <div style="font-size:11px; font-style:italic;">{data['patient']}</div>
                </div>
            """, unsafe_allow_html=True)
