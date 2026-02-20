import streamlit as st
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# ---------------- Sidebar ----------------
st.sidebar.title("🚧 Smart Pothole Reporting System")
st.sidebar.markdown("**Project Type:** Team Project")
st.sidebar.markdown("**Technology:** Python, Streamlit, GPS")
st.sidebar.markdown("**Function:** Location Safety Check")


# -----------------------------
# Sidebar Information
# -----------------------------
st.sidebar.title("📌 Project Details")

st.sidebar.markdown("### 🚧 Project Name")
st.sidebar.write("Smart Pothole Reporting System")

st.sidebar.markdown("### 👨‍👩‍👧‍👦 Team Members")
st.sidebar.write("""
- Kalyani Vanga
- Sneha Gayatri Mandapati 
- Srilakshmi Durga Undamatla
""")

st.sidebar.markdown("### 👨‍🏫 Guide Name")
st.sidebar.write("Abdul Aziz Md")

st.sidebar.markdown("---")
st.sidebar.caption("Academic Project")

# ---------------- Title ----------------
st.title("📍 Smart Pothole Reporting & Safety Check")
st.write("Enter a location to check whether the place is **safe or pothole-prone**.")

# Initialize geolocator
geolocator = Nominatim(user_agent="pothole_app")

# ---------------- Dummy Pothole Database ----------------
# (Sample pothole locations for project demo)
pothole_locations = [
    (17.3850, 78.4867),  # Hyderabad
    (17.4401, 78.3489),  # Gachibowli
    (17.4948, 78.3996)   # Kukatpally
]

# ---------------- Location Input ----------------
place = st.text_input("Enter Location (Area / City / Road Name):")

if st.button("Check Location Safety"):
    if place:
        location = geolocator.geocode(place)

        if location:
            user_location = (location.latitude, location.longitude)

            st.success("📍 Location Found")
            st.write("🌍 Latitude:", location.latitude)
            st.write("🌍 Longitude:", location.longitude)

            # Safety Check
            safe = True
            for pothole in pothole_locations:
                distance = geodesic(user_location, pothole).meters
                if distance <= 100:
                    safe = False
                    break

            if safe:
                st.success("✅ This place is SAFE. No potholes nearby.")
            else:
                st.error("⚠ ALERT! Pothole-prone area within 100 meters.")

        else:
            st.error("❌ Unable to fetch location")
    else:
        st.warning("⚠ Please enter a location")

# ---------------- Footer ----------------
st.markdown("---")
st.markdown("🚦 Smart Pothole Detection and Safety Alert System")
