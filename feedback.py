import streamlit as st
import datetime

def feedback_portal():
    st.title("💬 DVLA Spintex - Feedback & Complaints")

    menu = ["Submit Feedback", "Track Feedback"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Submit Feedback":
        st.subheader("📝 Submit Feedback or Complaint")
        email = st.text_input("Your Email")
        issue = st.text_area("Describe your issue or feedback")

        if st.button("Submit"):
            ticket_id = f"ticket_{int(datetime.datetime.now().timestamp())}"
            db.collection("feedback").document(ticket_id).set({
                "submitted_by": email,
                "issue": issue,
                "status": "open",
                "submitted_at": datetime.datetime.utcnow().isoformat()
            })
            st.success(f"✅ Feedback submitted! Your Ticket ID: {ticket_id}")

    elif choice == "Track Feedback":
        st.subheader("🔍 Track Feedback Status")
        ticket_id = st.text_input("Enter your Ticket ID")
        if st.button("Check Status"):
            doc = db.collection("feedback").document(ticket_id).get()
            if doc.exists:
                data = doc.to_dict()
                st.write(f"**Issue:** {data['issue']}")
                st.write(f"**Status:** {data['status']}")
                st.write(f"**Submitted by:** {data['submitted_by']}")
                st.write(f"**Submitted at:** {data['submitted_at']}")
            else:
                st.error("❌ Ticket not found. Please check your ID.")
