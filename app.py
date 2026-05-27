import streamlit as st

# -------------------------
# STATE
# -------------------------
if "risk_score" not in st.session_state:
    st.session_state.risk_score = 0

if "step" not in st.session_state:
    st.session_state.step = "normal"

if "beneficiary_ok" not in st.session_state:
    st.session_state.beneficiary_ok = False


# -------------------------
# ENGINE
# -------------------------
def add_risk(value):
    st.session_state.risk_score += value


def reset():
    st.session_state.risk_score = 0
    st.session_state.step = "normal"
    st.session_state.beneficiary_ok = False


def evaluate():
    score = st.session_state.risk_score

    if score >= 55:
        st.session_state.step = "suspended"
    elif score >= 35:
        st.session_state.step = "review"
    else:
        st.session_state.step = "normal"


st.title("🛡️ Adaptive Fraud Detection System")

st.metric("Risk Score", st.session_state.risk_score)

evaluate()

# -------------------------
# SIDEBAR SIGNALS
# -------------------------
st.sidebar.header("Behavior simulation")

if st.sidebar.button("New Device (+20)"):
    add_risk(20)

if st.sidebar.button("New Location (+15)"):
    add_risk(15)

if st.sidebar.button("High Amount (+30)"):
    add_risk(30)

if st.sidebar.button("Failed Attempts (+20)"):
    add_risk(20)

if st.sidebar.button("Reset"):
    reset()

evaluate()

# -------------------------
# LOW RISK
# -------------------------
if st.session_state.step == "normal":
    st.success("✅ Transaction approved")

    if st.button("Execute transaction"):
        st.success("💸 Transaction executed successfully")


# -------------------------
# MEDIUM RISK (35–54)
# -------------------------
elif st.session_state.step == "review":

    st.warning("⚠️ Suspicious behavior detected")

    st.info("Veuillez vérifier le bénéficiaire avant exécution")

    col1, col2 = st.columns(2)

    if col1.button("✅ Bénéficiaire vérifié"):
        st.session_state.beneficiary_ok = True
        st.success("Bénéficiaire validé")

    if col2.button("❌ Annuler transaction"):
        st.session_state.step = "cancelled"
        st.rerun()


# -------------------------
# HIGH RISK (>=55)
# -------------------------
elif st.session_state.step == "suspended":

    st.error("⏳ Transactions suspendues pour vérification")

    st.warning("Double authentification requise (3DS + bénéficiaire)")

    # Beneficiary check
    if st.button("✅ Confirmer bénéficiaire"):
        st.session_state.beneficiary_ok = True

    # 3DS
    otp = st.text_input("🔐 3DS Code (1234)")

    if st.button("Valider 3DS"):
        if st.session_state.beneficiary_ok and otp == "1234":
            st.session_state.step = "approved"
            st.rerun()
        else:
            st.error("Vérifications incomplètes ou OTP invalide")


# -------------------------
# APPROVED
# -------------------------
elif st.session_state.step == "approved":
    st.success("✅ Transaction exécutée après vérifications")


# -------------------------
# CANCELLED
# -------------------------
elif st.session_state.step == "cancelled":
    st.info("❌ Transaction annulée")
