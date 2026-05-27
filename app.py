#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 18:37:51 2026

@author: laraki
"""

import streamlit as st

# -------------------------
# INIT STATE
# -------------------------
if "risk_score" not in st.session_state:
    st.session_state.risk_score = 0

if "step" not in st.session_state:
    st.session_state.step = "normal"  # normal / review / 3ds / blocked / cancelled / approved


# -------------------------
# RISK ENGINE
# -------------------------
def add_risk(value):
    st.session_state.risk_score += value


def reset():
    st.session_state.risk_score = 0
    st.session_state.step = "normal"


def evaluate_risk():
    score = st.session_state.risk_score

    if score >= 70:
        st.session_state.step = "blocked"
    elif score >= 40:
        st.session_state.step = "review"
    else:
        st.session_state.step = "normal"


# -------------------------
# UI HEADER
# -------------------------
st.title("🛡️ Green-Got Fraud Detection Dashboard")
st.write("Real-time behavioral risk scoring & adaptive friction engine")

st.metric("Risk Score", st.session_state.risk_score)

evaluate_risk()


# -------------------------
# SIDEBAR - EVENTS
# -------------------------
st.sidebar.header("Simulate behavioral signals")

if st.sidebar.button("New Device Login (+20)"):
    add_risk(20)

if st.sidebar.button("New Geo-location (+15)"):
    add_risk(15)

if st.sidebar.button("New Beneficiary + Instant Transfer (+25)"):
    add_risk(25)

if st.sidebar.button("Night Operation (+10)"):
    add_risk(10)

if st.sidebar.button("Unusual Amount (+30)"):
    add_risk(30)

if st.sidebar.button("Failed Attempts / Probing (+20)"):
    add_risk(20)

if st.sidebar.button("Reset"):
    reset()


evaluate_risk()


# -------------------------
# MAIN LOGIC
# -------------------------

score = st.session_state.risk_score
step = st.session_state.step


# -------------------------
# LOW RISK
# -------------------------
if step == "normal":
    st.success("✅ Transaction status: APPROVED (low risk)")
    st.write("No friction applied.")

    if st.button("Execute Transaction"):
        st.success("💸 Transaction executed successfully")


# -------------------------
# MEDIUM RISK (>=40)
# PUSH + BENEFICIARY CHECK
# -------------------------
elif step == "review":

    st.warning("🚨 Suspicious activity detected")

    st.info("Opération suspecte, veuillez vérifier le bénéficiaire")

    col1, col2 = st.columns(2)

    if col1.button("✅ Bénéficiaire vérifié"):
        st.session_state.step = "3ds"
        st.rerun()

    if col2.button("❌ Annuler le paiement"):
        st.session_state.step = "cancelled"
        st.rerun()


# -------------------------
# 3DS STEP-UP AUTH
# -------------------------
elif step == "3ds":

    st.warning("🔐 3DS Authentication Required")

    st.write("Veuillez valider la transaction via 3DS (OTP / biométrie simulée)")

    otp = st.text_input("Enter OTP code")

    if st.button("Validate 3DS"):
        if otp == "1234":  # simulation
            st.session_state.step = "approved"
            st.rerun()
        else:
            st.error("Invalid OTP")


# -------------------------
# APPROVED AFTER 3DS
# -------------------------
elif step == "approved":
    st.success("✅ Transaction approved after 3DS authentication")
    st.balloons()


# -------------------------
# BLOCKED HIGH RISK
# -------------------------
elif step == "blocked":
    st.error("⛔ Transaction BLOCKED")
    st.write("Cooling-off period activated due to high fraud risk")


# -------------------------
# CANCELLED
# -------------------------
elif step == "cancelled":
    st.info("❌ Transaction cancelled by user")