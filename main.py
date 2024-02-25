import streamlit as st

# Placeholder for authentication function
def authenticate_user(username, password):
    # This is where you'd implement your actual authentication logic
    return username == "student" and password == "password"

# Initialize session state variables for navigation and authentication
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# Function to display the login form in the sidebar
def show_login_form():
    with st.sidebar:
        st.title("Login Section")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state['authenticated'] = True
                st.session_state['page'] = 'general'
                st.experimental_rerun()
            else:
                st.error("Invalid username/password")

# Function to display navigation options in the sidebar after login
def show_navigation():
    with st.sidebar:
        st.title("Navigation")
        if st.button("General Page"):
            st.session_state['page'] = 'general'
        if st.button("Dashboard Area"):
            st.session_state['page'] = 'dashboard'



import googlemaps

# Initialize your Google Maps client (Uncomment and set your API key)

gmaps = googlemaps.Client(key=st.secrets['google_maps_key'])
# Mock function to simulate fetching bars near a campus location
def fetch_bars_near_campus(campus_location):
    # Replace 'campus_location' with actual latitude and longitude
    # For example: campus_location = {'lat': 45.406435, 'lng': 11.876761} # Example coordinates
    
    # Making a request to find bars near the campus location
    places_result = gmaps.places_nearby(location=campus_location, radius=500, type='bar')
    
    bars = []
    for place in places_result.get('results', []):
        bars.append({
            'name': place.get('name'),
            'address': place.get('vicinity'),
            'rating': place.get('rating', 'N/A')
        })
    return bars



# Placeholder functions for each feature's detailed page
def show_bar_finder():
    st.header("Bar Finder (Gluten Free Bars)")
    st.write("Detailed information and functionality for finding gluten-free bars.")
    
    campuses = {
        'Campus A': {'lat': 45.411889, 'lng': 11.887048}, # DEI Department, University of Padova
        'Campus B': {'lat': 45.421500, 'lng': 11.886111}, # Psychology Department, University of Padova
    }
    
    
    campus_selection = st.selectbox("Select your campus", list(campuses.keys()))

    if st.button('Find Bars'):
        campus_location = campuses[campus_selection]
        bars = fetch_bars_near_campus(campus_location)
        if bars:
            for bar in bars:
                st.markdown(f"**{bar['name']}**")
                st.write(f"Address: {bar['address']}")
                st.write(f"Rating: {bar['rating']}")
        else:
            st.write("No bars found near this campus.")




def show_events_and_dei():
    st.header("Events & DEI Flyers")
    st.write("Detailed information on events and Diversity, Equity, and Inclusion (DEI) flyers.")

def show_news_and_tips():
    st.header("News & Tips")
    st.write("Latest news and tips for students.")

def show_study_group_finder():
    st.header("Study Group Finder")
    st.write("Functionality to find or create study groups.")

def show_course_recommendation():
    st.header("Course Recommendation System")
    st.write("System to recommend courses based on student preferences and history.")

# Main app logic
if not st.session_state['authenticated']:
    show_login_form()
else:
    show_navigation()
    
    if st.session_state['page'] == 'general':
        tab1, tab2, tab3 = st.tabs(["Bar Finder", "Events & DEI", "News & Tips"])
        with tab1:
            show_bar_finder()
        with tab2:
            show_events_and_dei()
        with tab3:
            show_news_and_tips()
    elif st.session_state['page'] == 'dashboard':
        tab1, tab2 = st.tabs(["Study Group Finder", "Course Recommendation"])
        with tab1:
            show_study_group_finder()
        with tab2:
            show_course_recommendation()