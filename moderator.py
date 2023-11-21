import streamlit as st
import database_utils as db

def show_moderator_dashboard():
    st.title("Moderator Dashboard")
    reports = db.get_reports()
    for report in reports:
        with st.expander(f"Report ID: {report['id']}"):
            st.write(f"Location: {report['location']}")
            st.write(f"Emergency Level: {report['emergency_level']}")
            # More report details...
            if st.button("Mark as Reviewed", key=report['id']):
                # Update report status in the database
                db.update_report_status(report['id'], 'REVIEWED')
                st.success("Report marked as reviewed.")
