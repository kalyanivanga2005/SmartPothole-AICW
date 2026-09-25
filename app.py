import streamlit as st
from pathlib import Path
from PIL import Image
from ultralytics import YOLO
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Smart Pothole Reporting System",
    page_icon="🚧",
    layout="wide"
)


# ============================================================
# LOAD TRAINED YOLO MODEL
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

model_path = BASE_DIR / "pothole_best_model.pt"

if not model_path.exists():

    st.error(
        "❌ Trained model not found!\n\n"
        "Please place 'pothole_best_model.pt' "
        "inside the same folder as app.py."
    )

    st.stop()

model = YOLO(str(model_path))


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚧 Smart Pothole Reporting System")

st.sidebar.markdown("**Project Type:** Team Project")
st.sidebar.markdown(
    "**Technology:** Python, Streamlit, GPS, YOLO"
)
st.sidebar.markdown(
    "**Function:** Pothole Detection & Safety Alert"
)

st.sidebar.markdown("---")

st.sidebar.title("📌 Project Details")

st.sidebar.markdown("### 🚧 Project Name")
st.sidebar.write(
    "Smart Pothole Reporting System"
)

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

st.sidebar.write("""
- 🤖 AI/ML pothole detection
- 📍 Location-based safety checking
- 🌍 GPS latitude and longitude
- 📏 Distance calculation
- 🚨 Safety alert
""")


# ============================================================
# MAIN TITLE
# ============================================================

st.title(
    "📍 Smart Pothole Reporting & Safety Alert System"
)

st.write(
    "Upload a road image to detect potholes using "
    "the trained YOLO model and check whether a "
    "pothole-prone location is nearby."
)


# ============================================================
# STEP 1 — POTHOLE DETECTION
# ============================================================

st.markdown("## 🚧 Step 1: Pothole Detection")

uploaded_file = st.file_uploader(
    "Upload a road image",
    type=["jpg", "jpeg", "png"]
)


# Variable used later for safety alert
pothole_detected = False


if uploaded_file is not None:

    # --------------------------------------------------------
    # Open image
    # --------------------------------------------------------

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Road Image",
        use_container_width=True
    )

    # --------------------------------------------------------
    # Detect button
    # --------------------------------------------------------

    if st.button(
        "🔍 Detect Pothole",
        key="detect_button"
    ):

        with st.spinner(
            "🤖 AI/ML model is detecting potholes..."
        ):

            results = model.predict(
                source=image,
                conf=0.25
            )

        # ----------------------------------------------------
        # Check detection
        # ----------------------------------------------------

        if len(results[0].boxes) > 0:

            pothole_detected = True

            st.error(
                "🚧 POTHOLE DETECTED BY AI/ML!"
            )

            st.write(
                f"Number of potholes detected: "
                f"**{len(results[0].boxes)}**"
            )

            # Create annotated image
            annotated_image = results[0].plot()

            st.image(
                annotated_image,
                caption="🤖 AI/ML Pothole Detection Result",
                use_container_width=True
            )

        else:

            pothole_detected = False

            st.success(
                "✅ No pothole detected in the uploaded image."
            )


# ============================================================
# STEP 2 — LOCATION SAFETY CHECK
# ============================================================

st.markdown("---")

st.markdown(
    "## 📍 Step 2: Location Safety Check"
)

st.write(
    "Enter the area, city or road name where "
    "the client/user is currently located."
)


# ------------------------------------------------------------
# Geocoder
# ------------------------------------------------------------

geolocator = Nominatim(
    user_agent="smart_pothole_reporting_system"
)


# ============================================================
# SAMPLE POTHOLE GPS DATABASE
# ============================================================
#
# These are sample locations for academic demonstration.
#
# In a real application, these coordinates should come
# from a database containing reported pothole locations.
# ============================================================

pothole_locations = [
    {
        "name": "Hyderabad",
        "latitude": 17.3850,
        "longitude": 78.4867
    },

    {
        "name": "Gachibowli",
        "latitude": 17.4401,
        "longitude": 78.3489
    },

    {
        "name": "Kukatpally",
        "latitude": 17.4948,
        "longitude": 78.3996
    }
]


# ============================================================
# LOCATION INPUT
# ============================================================

place = st.text_input(
    "Enter Location (Area / City / Road Name):",
    placeholder="Example: Hyderabad"
)


# ============================================================
# CHECK LOCATION BUTTON
# ============================================================

if st.button(
    "📍 Check Location Safety",
    key="location_button"
):

    if place.strip() == "":

        st.warning(
            "⚠️ Please enter the client location."
        )

    else:

        with st.spinner(
            "🌍 Finding location..."
        ):

            location = geolocator.geocode(
                place
            )


        # ----------------------------------------------------
        # Location found
        # ----------------------------------------------------

        if location:

            user_location = (
                location.latitude,
                location.longitude
            )

            st.success(
                "📍 Location Found"
            )

            st.write(
                "🌍 Latitude:",
                location.latitude
            )

            st.write(
                "🌍 Longitude:",
                location.longitude
            )


            # =================================================
            # FIND NEAREST POTHOLE
            # =================================================

            nearest_pothole = None
            nearest_distance = float("inf")


            for pothole in pothole_locations:

                pothole_location = (
                    pothole["latitude"],
                    pothole["longitude"]
                )

                distance = geodesic(
                    user_location,
                    pothole_location
                ).meters


                if distance < nearest_distance:

                    nearest_distance = distance
                    nearest_pothole = pothole


            # =================================================
            # DISPLAY NEAREST POTHOLE
            # =================================================

            if nearest_pothole is not None:

                st.info(
                    f"📏 Nearest sample pothole location: "
                    f"**{nearest_pothole['name']}**"
                )

                st.write(
                    f"📏 Distance: "
                    f"**{nearest_distance:.2f} meters**"
                )


                # =================================================
                # SAFETY CHECK
                # =================================================

                if nearest_distance <= 100:

                    # ---------------------------------------------
                    # POTHOLE IS NEARBY
                    # ---------------------------------------------

                    st.error(
                        "🚨 ALERT! POTHOLE IS NEARBY!"
                    )

                    st.warning(
                        "⚠️ Please slow down and drive carefully."
                    )

                    st.toast(
                        "🚨 Pothole nearby! Drive carefully!",
                        icon="⚠️"
                    )


                    # ---------------------------------------------
                    # Combine GPS + AI result
                    # ---------------------------------------------

                    if pothole_detected:

                        st.error(
                            "🤖 AI detected a pothole in "
                            "the uploaded road image."
                        )

                        st.success(
                            "🚨 SAFETY ALERT ACTIVATED!"
                        )

                    else:

                        st.info(
                            "📍 A pothole-prone location "
                            "was found within 100 meters."
                        )


                else:

                    # ---------------------------------------------
                    # POTHOLE IS FAR
                    # ---------------------------------------------

                    st.success(
                        "✅ SAFE: No sample pothole "
                        "within 100 meters."
                    )


                    # ---------------------------------------------
                    # AI pothole but GPS location is far
                    # ---------------------------------------------

                    if pothole_detected:

                        st.warning(
                            "🤖 A pothole was detected in "
                            "the uploaded image, but the "
                            "selected location is more than "
                            "100 meters from the sample "
                            "pothole locations."
                        )


        # ----------------------------------------------------
        # Location not found
        # ----------------------------------------------------

        else:

            st.error(
                "❌ Unable to find the entered location."
            )


# ============================================================
# PROJECT FLOW
# ============================================================

st.markdown("---")

st.markdown("## 🔄 System Workflow")

st.write("""
1. 📷 User uploads a road image.
2. 🤖 YOLO model detects potholes.
3. 📍 User enters the current location.
4. 🌍 Location is converted into latitude and longitude.
5. 📏 Distance from sample pothole locations is calculated.
6. 🚨 If a pothole is within 100 meters, a safety alert is shown.
7. ⚠️ User is advised to slow down and drive carefully.
""")


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    "🚦 **Smart Pothole Detection and Safety Alert System**"
)

st.caption(
    "AI/ML + YOLO + GPS + Distance Calculation + Safety Alert"
)
