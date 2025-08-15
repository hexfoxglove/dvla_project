import streamlit as st
from auth_client import sign_in, sign_up
from roles import get_user_role, set_user_role
from customer_portal import customer_portal
from feedback import feedback_portal
from dvla_admin_portal import dvla_admin_portal

st.set_page_config(page_title="DVLA Spintex Dashboard", page_icon="🚘", layout="centered")

def logout():
    for key in ["auth_id_token", "auth_uid", "user_email", "user_role", "authed"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def login_view():
    st.title("🔐 DVLA Spintex — Sign In")
    tab1, tab2 = st.tabs(["Sign In", "Create Account"])

    # ---------------- Sign In Tab ----------------
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Sign In"):
            id_token, refresh_token, uid = sign_in(email, password)
            if id_token:
                st.session_state.update({
                    "auth_id_token": id_token,
                    "auth_uid": uid,
                    "user_email": email,
                    "user_role": get_user_role(uid),
                    "authed": True
                })
                st.rerun()
            else:
                st.error("Invalid email or password.")

    # ---------------- Sign Up Tab ----------------
    with tab2:
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password (min 6 chars)", type="password", key="signup_password")
        role = st.selectbox("Role", ["customer", "staff", "admin"])  # In production, restrict this
        if st.button("Create Account"):
            id_token, refresh_token, uid = sign_up(email, password)
            if id_token:
                set_user_role(uid, email, role)
                st.success("✅ Account created! Please sign in.")
            else:
                st.error("❌ Sign up failed. Try a different email/password.")

def route_by_role(role: str):
    st.sidebar.write(f"**Role:** {role}")
    st.sidebar.button("Logout", on_click=logout)

    if role == "customer":
        choice = st.sidebar.radio("Menu", ["Customer Portal", "Feedback"])
        if choice == "Customer Portal":
            customer_portal()
        else:
            feedback_portal()

    elif role in ["staff", "admin"]:
        choice = st.sidebar.radio("Menu", ["Admin Dashboard", "Feedback", "Customer Portal"])
        if choice == "Admin Dashboard":
            dvla_admin_portal()
        elif choice == "Customer Portal":
            customer_portal()
        else:
            feedback_portal()

def main():
    st.markdown("<h2 style='text-align:center'>DVLA Spintex Localized Dashboard</h2>", unsafe_allow_html=True)
    if not st.session_state.get("authed"):
        login_view()
    else:
        route_by_role(st.session_state["user_role"])

if __name__ == "__main__":
    main()
