import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json

# Page Config
st.set_page_config(page_title="GEIMS ICU Tracker", layout="wide")

# --- 0. PROFESSIONAL HEADER ---
st.markdown("<h1 style='text-align: center; color: white;'>Graphic Era Institute of Medical Sciences - GEIMS, Dehradun</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #ADD8E6;'>Critical Care & ICU Dashboard</h3>", unsafe_allow_html=True)
st.divider()

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

# --- 2. SPECIALTY-WISE ICU STRUCTURE (FIXED) ---
icu_structure = {
    "8th Floor - RICU - 8th C": ["B-ICU-20", "B-ICU-17", "B-ICU-18", "MICU-1", "MICU-2", "MICU-3", "MICU-4", "MICU-5", "SICU-1", "SICU-2", "SICU-3", "SICU-4", "SICU-5", "RICU-1", "RICU-2", "RICU-3", "RICU-4", "RICU-5", "B-ICU-31", "B-ICU-27"],
    "8th Floor - Respiratory ICU (8th E)": ["ICU-8F-1", "ICU-8F-2", "ICU-8F-3", "ICU-8F-4", "ICU-8F-5", "ICU-8F-6", "ICU-8F-7", "ICU-8F-8", "ICU-8F-9", "ICU-8F-10"],
    "8th Floor - MICU (8th D)": ["MICU-1", "MICU-2", "MICU-3", "MICU-4", "MICU-5", "MICU-6", "MICU-7", "MICU-8", "MICU-9", "MICU-10", "MICU-11", "MICU-12", "MICU-14"],
    "8th Floor - Neuro SICU (8th F)": ["N-SICU-1", "N-SICU-2", "N-SICU-3", "N-SICU-4", "N-SICU-5", "N-SICU-6", "N-SICU-7", "N-SICU-8", "N-SICU-9", "N-SICU-10", "N-SICU-11", "N-SICU-12", "N-SICU-13", "N-SICU-14", "N-SICU-15"],
    "8th Floor - Neuro HDU (8th A)": ["GF-Neuro HDU-1", "GF-Neuro HDU-2", "GF-Neuro HDU-3", "GF-Neuro HDU-4", "GF-Neuro HDU-5", "GF-Neuro HDU-6", "GF-Neuro HDU-7", "GF-Neuro HDU-8", "GF-Neuro HDU-9", "GF-Neuro HDU-10", "GF-Neuro HDU-11", "GF-Neuro HDU-12", "GF-Neuro HDU-16", "GF-Neuro HDU-14", "GF-Neuro HDU-15"],
    "6th Floor - Medicine HDU (6th B)": [
        "HDU-1", "HDU-2", "HDU-3", "HDU-4", "HDU-5", "HDU-6", "HDU-7", "HDU-8", "HDU-9", "HDU-10",
        "HDU-11", "HDU-12", "HDU-14", "HDU-15", "HDU-16", "HDU-17", "HDU-18", "HDU-19", "HDU-20",
        "HDU-21", "HDU-22", "HDU-23", "HDU-24", "HDU-25", "HDU-26", "HDU-27", "HDU-28", "HDU-29", "HDU-30", "HDU-31"
    ],
    "6th Floor - Ayushman ICU (6th E)": ["PMJAY-1", "PMJAY-2", "PMJAY-3", "PMJAY-4", "PMJAY-5", "PMJAY-6", "PMJAY-7", "PMJAY-8", "ICU-9", "PMJAY-9", "PMJAY-10", "PMJAY-11", "PMJAY-12", "PMJAY-13", "PMJAY-14", "PMJAY-15", "PMJAY-16", "PMJAY-17", "PMJAY-18", "PMJAY-19", "PMJAY-20", "PMJAY-21", "PMJAY-22", "PMJAY-23", "PMJAY-24"],
    "4th Floor - Surgical ICU 2 (4th F)": ["SICU 2-7", "SICU 2-8", "SICU 2-1", "SICU 2-2", "SICU 2-3", "SICU 2-4", "SICU 2-5", "SICU 2-6", "Burn ICU-1", "Burn ICU-2"],
    "4th Floor - CCU-1": ["ccu-121", "B-CCU-1", "B-CCU-2", "B-CCU-3", "B-CCU-4", "B-CCU-5", "B-CCU-6", "B-CCU-7", "B-CCU-8", "B-CCU-9", "B-CCU-10", "B-CCU-11", "B-CCU-12", "B-CCU-16", "B-CCU-14", "B-CCU-15"],
    "4th Floor - CTVS & CCU-2": ["CTVS-1", "CTVS-2", "CTVS-3", "CTVS-4", "CTVS-5", "CTVS-6", "CTVS-7", "CTVS-8", "CTVS-9", "CTVS-10", "CCU-2-1", "CCU-2-2", "CCU-2-3", "CCU-2-4", "CCU-2-5", "CCU-2-6", "CCU-2-7", "CCU-2-8", "CCU-2-9", "CCU-2-10"],
    "Ground Floor - PICU": ["PICU-7", "PICU-1", "PICU-2", "PICU-3", "PICU-4", "PICU-5", "PICU-6"]
}

# --- 3. ADMIN PANEL ---
with st.sidebar:
    st.header("🔐 ICU Admin Portal")
    pwd = st.text_input("Admin Password", type="password")
    is_admin = (pwd == "Geims248001")
    if is_admin:
        all_ids = [b for w in icu_structure.values() for b in w]
        sel_bed = st.selectbox("Select ICU/HDU Bed", sorted(list(set(all_ids))))
        new_stat = st.selectbox("Status", ["VACANT", "OCCUPIED", "BOOKED", "SHIFTING", "VENTILATOR ON", "CRITICAL", "TO DISCHARGE", "MAINTENANCE"])
        p_name = st.text_input("Patient Name")
        if st.button("Update Status Permanently"):
            db.collection("icu_beds").document(sel_bed).set({"status": new_stat, "patient": p_name})
            st.success(f"Updated {sel_bed}")
            st.rerun()

# --- 4. DASHBOARD ---
docs = db.collection("icu_beds").stream()
live_data = {doc.id: doc.to_dict() for doc in docs}
status_colors = {
    "VACANT": "#FFFFFF", "OCCUPIED": "#000000", "BOOKED": "#90EE90", 
    "SHIFTING": "#FFA500", "VENTILATOR ON": "#1E90FF", "CRITICAL": "#B22222", 
    "TO DISCHARGE": "#ADD8E6", "MAINTENANCE": "#E0E0E0"
}

for unit, beds in icu_structure.items():
    st.subheader(unit)
    cols = st.columns(6)
    for i, bed in enumerate(beds):
        data = live_data.get(bed, {"status": "VACANT", "patient": ""})
        bg = status_colors.get(data['status'], "#FFFFFF")
        txt = "white" if data['status'] in ["OCCUPIED", "CRITICAL", "VENTILATOR ON"] else "black"
        with cols[i % 6]:
            st.markdown(f'<div style="background-color:{bg}; color:{txt}; padding:10px; border:1px solid #ccc; border-radius:5px; text-align:center; height:110px; margin-bottom:10px;"><div style="font-size:11px; font-weight:bold;">{bed}</div><div style="font-size:10px;">{data["status"]}</div><div style="font-size:10px; font-style:italic;">{data["patient"]}</div></div>', unsafe_allow_html=True)
    st.divider()
