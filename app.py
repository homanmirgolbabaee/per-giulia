import streamlit as st
from moderator import show_moderator_dashboard
import database_utils as db
import bcrypt 

# Example login function
def login_user(username, password):
    # Fetch user details from the database
    user = db.get_user(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        return user
    else:
        return None

    
    
# Login form
with st.sidebar:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state['user'] = user
            st.success("Logged in successfully!")
            user_role = user['role']  # Dynamically determine user role
        else:
            st.error("Invalid username or password")


st.title("Campus Safety Reporting System")



# Show moderator dashboard if user role is 'moderator'
if 'user' in st.session_state and st.session_state['user'].get('role') == "moderator":
    from moderator import show_moderator_dashboard
    show_moderator_dashboard()

if 'user' in st.session_state and st.session_state['user'].get('role') == "user":
    from user import submit_report
    submit_report()
    
if 'user' in st.session_state and st.session_state['user'].get('role') == "employee":
    from employee import employee_dashboard
    employee_dashboard()