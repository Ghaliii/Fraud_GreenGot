import streamlit as st

# -------------------------
# STATE INIT
# -------------------------
if "risk_score" not in st.session_state:
    st.session_state.risk_score = 0

if "step" not in st.session_state:
    st.session_state.step = "normal"

if "beneficiary_ok" not in st.session_state:
    st.session_state.beneficiary_ok = False

if "otp_ok" not in st.session_state:
    st.session_state.otp_ok = False


# -------------------------
# RISK ENGINE (FIXED VALUES)
# -------------------------
def add_risk(value):
    st.session_state.risk_score += value


def reset():
    st.session_state.risk_score = 0
    st.session_state.step = "normal"
    st.session_state.beneficiary_ok = False
    st.session_state.otp_ok = False


def evaluate():
    score = st.session_state.risk_score

    if score >= 55:
        st.session_state.step = "suspended"
    elif score >= 35:
        st.session_state.step = "review"
    else:
        st.session_state.step = "normal"


# -------------------------
# UI
# -------------------------
st.title("🛡️ Fraud Detection Engine (Adaptive Risk Model)")
st.metric("Risk Score", st.session_state.risk_score)

evaluate()

# -------------------------
# SIDEBAR EVENTS (FIXED VALUES)
# -------------------------
st.sidebar.header("Behavioral signals")

if st.sidebar.button("New Device (+20)"):
    add_risk(20)

if st.sidebar.button("New Location (+15)"):
    add_risk(15)

if st.sidebar.button("New Beneficiary + Instant Transfer (+25)"):
    add_risk(25)

if st.sidebar.button("Night Operation (+10)"):
    add_risk(10)

if st.sidebar.button("Unusual Amount (+30)"):
    add_risk(30)

if st.sidebar.button("Failed Attempts (+20)"):
    add_risk(20)

if st.sidebar.button("Reset"):
    reset()

evaluate()

# -------------------------
# ALWAYS REQUIRED: 3DS FUNCTION
# -------------------------
def render_3ds():
    otp = st.text_input("🔐 3DS Code (hint: 1234)")

    if st.button("Validate 3DS"):
        if otp == "1234":
            st.session_state.otp_ok = True
            st.success("3DS validated")
        else:
            st.error("Invalid OTP")


# -------------------------
# LOW RISK (<35)
# -------------------------
if st.session_state.step == "normal":

    st.success("✅ Transaction allowed")

    st.warning("🔐 3DS required for all transactions")

    render_3ds()

    if st.session_state.otp_ok and st.button("Execute transaction"):
        st.success("💸 Transaction executed successfully")


# -------------------------
# MEDIUM RISK (35–54)
# -------------------------
elif st.session_state.step == "review":

    st.warning("⚠️ Medium risk transaction")

    st.info("🔎 Vérification bénéficiaire obligatoire")

    if st.button("✅ Confirmer bénéficiaire"):
        st.session_state.beneficiary_ok = True

    st.warning("🔐 3DS required")

    render_3ds()

    if st.session_state.beneficiary_ok and st.session_state.otp_ok:

        if st.button("Execute transaction"):
            st.success("💸 Transaction executed after verification")


# -------------------------
# HIGH RISK (>=55)
# -------------------------
elif st.session_state.step == "suspended":

    st.error("⏳ Transaction temporairement suspendue")

    st.info("Double vérification obligatoire (beneficiary + 3DS)")

    if st.button("✅ Confirmer bénéficiaire"):
        st.session_state.beneficiary_ok = True

    render_3ds()

    if st.session_state.beneficiary_ok and st.session_state.otp_ok:

        if st.button("Release transaction"):
            st.success("💸 Transaction released after suspension")
