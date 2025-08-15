import streamlit as st
from firebase_config import db
import datetime
import pandas as pd

def dvla_admin_portal():
    st.title("🛠 DVLA Spintex - Admin Dashboard")

    menu = ["Manage Requests", "Manage Feedback", "Manage Appointments", "View Analytics"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Manage Requests":
        st.subheader("📋 Customer Requests")
        requests = db.collection("customer_requests").stream()
        for doc in requests:
            data = doc.to_dict()
            st.write(f"**Request ID:** {doc.id}")
            st.write(f"Name: {data['name']}")
            st.write(f"Vehicle: {data['vehicle_reg']}")
            st.write(f"Service: {data['service_type']}")
            st.write(f"Status: {data['status']}")
            new_status = st.selectbox(f"Update status for {doc.id}", 
                                      ["pending", "in progress", "completed", "rejected"], 
                                      index=["pending", "in progress", "completed", "rejected"].index(data["status"]))
            if st.button(f"Save Request {doc.id}"):
                db.collection("customer_requests").document(doc.id).update({"status": new_status})
                st.success(f"✅ Status updated for {doc.id}")
            st.write("---")

    elif choice == "Manage Feedback":
        st.subheader("💬 Customer Feedback & Complaints")
        tickets = db.collection("feedback").stream()
        for doc in tickets:
            data = doc.to_dict()
            st.write(f"**Ticket ID:** {doc.id}")
            st.write(f"Issue: {data['issue']}")
            st.write(f"Status: {data['status']}")
            new_status = st.selectbox(f"Update status for {doc.id}", 
                                      ["open", "in progress", "resolved"], 
                                      index=["open", "in progress", "resolved"].index(data["status"]))
            if st.button(f"Save Ticket {doc.id}"):
                db.collection("feedback").document(doc.id).update({"status": new_status})
                st.success(f"✅ Ticket {doc.id} updated")
            st.write("---")

    elif choice == "Manage Appointments":
        st.subheader("📅 Appointments")
        appointments = db.collection("appointments").stream()
        for doc in appointments:
            data = doc.to_dict()
            st.write(f"**Appointment ID:** {doc.id}")
            st.write(f"Name: {data['name']}")
            st.write(f"Purpose: {data['purpose']}")
            st.write(f"Preferred Time: {data['preferred_time']}")
            st.write(f"Status: {data.get('status', 'pending')}")
            new_status = st.selectbox(f"Update status for {doc.id}", 
                                      ["pending", "confirmed", "completed", "cancelled"], 
                                      index=["pending", "confirmed", "completed", "cancelled"].index(data.get("status", "pending")))
            if st.button(f"Save Appointment {doc.id}"):
                db.collection("appointments").document(doc.id).update({"status": new_status})
                st.success(f"✅ Appointment {doc.id} updated")
            st.write("---")

    elif choice == "View Analytics":
        st.subheader("📊 Dashboard Analytics")
        requests = db.collection("customer_requests").stream()
        data_list = []
        for doc in requests:
            data = doc.to_dict()
            data_list.append({
                "submitted_at": data["submitted_at"],
                "status": data["status"]
            })
        if data_list:
            df = pd.DataFrame(data_list)
            df["submitted_at"] = pd.to_datetime(df["submitted_at"])
            daily_counts = df.groupby(df["submitted_at"].dt.date).size()
            st.bar_chart(daily_counts)
        else:
            st.info("No request data available yet.")
