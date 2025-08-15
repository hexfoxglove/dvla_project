import streamlit as st
from firebase_config import db
import datetime

def customer_portal():
    st.title("🚗 DVLA Spintex - Customer Portal")

    menu = ["Add Service Request", "View My Requests", "Book Appointment", "View My Appointments"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Service Request":
        st.subheader("📄 New Vehicle Service Request")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        vehicle_reg = st.text_input("Vehicle Registration Number")
        service_type = st.selectbox("Service Type", 
                                    ["Registration", "Renewal", "License Replacement"])

        if st.button("Submit Request"):
            request_id = f"req_{int(datetime.datetime.now().timestamp())}"
            db.collection("customer_requests").document(request_id).set({
                "name": name,
                "email": email,
                "vehicle_reg": vehicle_reg,
                "service_type": service_type,
                "status": "pending",
                "submitted_at": datetime.datetime.utcnow().isoformat()
            })
            st.success(f"✅ Request submitted! Your ID: {request_id}")

    elif choice == "View My Requests":
        st.subheader("📋 My Requests")
        email = st.text_input("Enter your email to view requests")
        if st.button("Search Requests"):
            docs = db.collection("customer_requests").where("email", "==", email).stream()
            for doc in docs:
                data = doc.to_dict()
                st.write(f"**Request ID:** {doc.id}")
                st.write(f"Vehicle: {data['vehicle_reg']}")
                st.write(f"Service: {data['service_type']}")
                st.write(f"Status: {data['status']}")
                st.write("---")

    elif choice == "Book Appointment":
        st.subheader("📅 Book Appointment")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        purpose = st.selectbox("Purpose", ["Registration", "Renewal", "License Replacement"])
        preferred_time = st.datetime_input("Preferred Date & Time")

        if st.button("Book Appointment"):
            appt_id = f"appt_{int(datetime.datetime.now().timestamp())}"
            db.collection("appointments").document(appt_id).set({
                "name": name,
                "email": email,
                "purpose": purpose,
                "preferred_time": preferred_time.isoformat(),
                "status": "pending"
            })
            st.success(f"✅ Appointment booked! ID: {appt_id}")

    elif choice == "View My Appointments":
        st.subheader("📋 My Appointments")
        email = st.text_input("Enter your email to view appointments")
        if st.button("Search Appointments"):
            docs = db.collection("appointments").where("email", "==", email).stream()
            for doc in docs:
                data = doc.to_dict()
                st.write(f"**Appointment ID:** {doc.id}")
                st.write(f"Purpose: {data['purpose']}")
                st.write(f"Preferred Time: {data['preferred_time']}")
                st.write(f"Status: {data.get('status', 'pending')}")
                st.write("---")
