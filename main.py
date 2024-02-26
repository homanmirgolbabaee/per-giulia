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
    #places_result = gmaps.places_nearby(location=campus_location, radius=500, type='bar')
    places_result = gmaps.places_nearby(location=campus_location, radius=500, type='bar', keyword='bar')
    bars = []
    for place in places_result.get('results', []):
        # Initialize photo_reference as None
        photo_reference = None
        # Check if 'photos' field is present and has at least one photo
        if 'photos' in place and len(place['photos']) > 0:
            photo_reference = place['photos'][0]['photo_reference']

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
        'DEI Campus': {'lat': 45.411889, 'lng': 11.887048}, # DEI Department, University of Padova
        'Pyschology Department': {'lat': 45.421500, 'lng': 11.886111}, # Psychology Department, University of Padova
        'Agripolis Campus': {'lat': 45.346337983376486, 'lng': 11.956815361663871} # Agripolis Campus, University of Padova
    }
    
    
    campus_selection = st.selectbox("Select your campus", list(campuses.keys()))

    if st.button('Find Bars'):
        campus_location = campuses[campus_selection]
        bars = fetch_bars_near_campus(campus_location)
        if bars:
            for bar in bars:
                # Use columns to create a more structured layout
                col1, col2 = st.columns([1, 4])
                with col1:
                    # Use the photo reference to fetch and display the image
                    if bar.get('photo_reference'):
                        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=100&photoreference={bar['photo_reference']}&key={st.secrets['google_maps_key']}"
                        st.image(photo_url, caption="Bar Image")
                    else:
                        # Display a placeholder if no photo is available
                        st.image("https://via.placeholder.com/100", caption="No Image Available")            
                        
                with col2:
                    st.markdown(f"#### {bar['name']}")
                    st.write(f"**Address:** {bar['address']}")
                    st.write(f"**Rating:** {bar['rating']}/5")
                    # Example of how you might add a link for directions
                    # You would need to construct the URL using the bar's actual coordinates or address
                    st.markdown(f"[Get Directions](https://www.google.com/maps/dir/?api=1&destination={bar['address'].replace(' ', '+')})")
        else:
            st.warning("No bars found near this campus. Try another campus or widen your search criteria.")




def show_events_and_dei():
    st.header("Events & DEI Flyers")
    st.write("Explore our latest events and Diversity, Equity, and Inclusion (DEI) initiatives through these flyers. Click on any image for more details.")

    # Assuming your images are named appropriately within the ./images/sources/ directory
    image_paths = [
        "sources/images/1.jpg",
        "sources/images/2.jpg",
        "sources/images/3.jpg",
        "sources/images/4.jpg"
    ]
    
    # Create a grid layout for the images - adjust the number of columns as per your UI design
    cols = st.columns(2) # This creates a 2-column layout; change the number inside columns() for a different layout
    
    for index, image_path in enumerate(image_paths):
        with cols[index % 2]: # This ensures distribution across the columns
            image = st.image(image_path, use_column_width=True) # Adjust use_column_width as needed
            # Optional: Add a caption or a button for more details under each image
            st.write("Event/DEI Initiative #{}".format(index + 1))
            # Example of adding a button that could, in future, link to more details
            if st.button('More Info', key=f'more_info_{index}'):
                st.write(f"You clicked for more information on item #{index + 1}.") # Placeholder for more info logic


def show_news_and_tips():
    st.header("News & Tips")
    st.subheader("Stay updated with the latest from Computer Engineering DEI")

    # Example of static news items - these could be fetched from a live database or API
    news_items = [
        {
            "title": "Diversity in Tech: Bridging the Gap",
            "date": "2024-02-25",
            "description": "A look into how the University of Padova is leading initiatives to bridge the diversity gap in tech.",
            "link": "https://www.example.com/news/1"
        },
        {
            "title": "Inclusive AI: Workshop Series",
            "date": "2024-03-05",
            "description": "Join our workshop series on developing inclusive AI technologies, hosted by the DEI department.",
            "link": "https://www.example.com/news/2"
        },
        {
            "title": "Tips for Aspiring Engineers",
            "date": "2024-03-10",
            "description": "Top tips and resources for students pursuing a career in computer engineering.",
            "link": "https://www.example.com/news/3"
        }
    ]

    # Display each news item using a card-like format
    for item in news_items:
        with st.container():
            st.markdown(f"### [{item['title']}]({item['link']})")
            st.caption(item['date'])
            st.write(item['description'])
            st.markdown(f"[Read more]({item['link']})")

    st.markdown("---")

    # Additional section for tips or resources
    st.subheader("Useful Resources")
    st.write("Explore a curated list of resources to aid your learning and development:")
    resources = [
        "[Learn Python for Data Science](https://www.example.com/resources/python)",
        "[Understanding Machine Learning Algorithms](https://www.example.com/resources/ml)",
        "[Career Paths in Computer Engineering](https://www.example.com/resources/careers)"
    ]
    for resource in resources:
        st.markdown(f"- {resource}")

def show_study_group_finder():
    st.header("Study Group Finder")
    st.subheader("Find or create study groups to enhance your learning experience.")

    # Input for specifying study interests
    interests = st.multiselect(
        "Select your study interests",
        ["Mathematics", "Science", "Engineering", "Programming", "Humanities", "Languages", "Other"],
        help="Select one or more areas you're interested in studying."
    )

    # Input for preferred study times
    study_times = st.multiselect(
        "Preferred study times",
        ["Morning", "Afternoon", "Evening", "No Preference"],
        help="Select one or more preferred study times."
    )

    # Input for preferred mode of communication
    communication_mode = st.selectbox(
        "Preferred mode of communication",
        ["Online (Zoom, Discord, etc.)", "In-person", "Either"],
        help="Choose your preferred mode of communication for study groups."
    )

    # Button to find study groups
    if st.button("Find Study Groups"):
        # Placeholder for search functionality
        st.write("Searching for study groups matching your criteria...")
        # Here, you would typically query a database or other data source to find matching groups.
        # For demonstration purposes, we'll just show a placeholder message.
        st.info("Feature to display matching study groups is under development.")

    st.markdown("---")

    # Section to create a new study group
    st.subheader("Create a New Study Group")
    group_name = st.text_input("Study Group Name", help="Give your study group a name.")
    group_description = st.text_area("Group Description", help="Describe what your study group will focus on.")

    # Button to create a new study group
    if st.button("Create Study Group"):
        # Placeholder for group creation functionality
        st.success(f"Study Group '{group_name}' created successfully!")
        # Here, you would typically save the new group details to a database or other data source.
        # Display a success message for now.
        # In a real application, implement the logic to save the group information.

def show_course_recommendation():
    st.header("Course Recommendation System")
    st.subheader("Find courses tailored to your interests, goals, and academic history.")

    # Input for specifying academic interests
    academic_interests = st.multiselect(
        "Select your academic interests",
        ["Computer Science", "Data Science", "Business", "Engineering", "Arts & Humanities", "Science", "Other"],
        help="Select one or more academic areas you're interested in."
    )

    # Input for specifying learning goals
    learning_goals = st.multiselect(
        "What are your learning goals?",
        ["Gain new skills", "Prepare for a career", "Explore new subjects", "Academic requirement", "Other"],
        help="Select one or more goals for your learning journey."
    )

    # Input for preferred course difficulty
    difficulty_level = st.selectbox(
        "Preferred difficulty level",
        ["Beginner", "Intermediate", "Advanced"],
        help="Choose the difficulty level suitable for your current knowledge and skills."
    )

    # Button to get course recommendations
    if st.button("Get Recommendations"):
        # Placeholder for recommendation functionality
        st.write("Generating personalized course recommendations...")
        # Here, you would typically query a recommendation engine or database to find courses that match the criteria.
        # For demonstration purposes, we'll just show a placeholder message.
        st.info("Feature to display personalized course recommendations is under development.")

    st.markdown("---")

    # Section to rate or provide feedback on recommendations (for future improvement)
    st.subheader("Rate or Provide Feedback on Recommendations")
    feedback_text = st.text_area("Feedback", help="Your feedback helps us improve future recommendations.")
    
    # Button to submit feedback
    if st.button("Submit Feedback"):
        # Placeholder for feedback submission functionality
        st.success("Thank you for your feedback!")
        # In a real application, you would store this feedback for analysis and improvement of the recommendation algorithm.

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
