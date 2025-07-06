import requests
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from get_image import get_image
import time

load_dotenv()

# Constants
API_URL = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"
API_KEY = "g3iPHWSLfm2yd9bBzy8C25GEZ8r276Ha9ekLTLsQ"

EXEMPTION_LIST = sorted([
    "Maintenance, B1+B2+B6.", "Royal Mail, B3.", "Bus, D.", "Emergency, E.",
    "Disabled Badge, K1-3.", "WAHC (Taxi), N4.", "Permit, R1+R2.",
    "Permit, R8+R9.", "NET Maintenance, T2+T3.", "ULEV, U.", "Permit, U1.",
    "Security Vehicle, V.", "Private Hire, W1.", "Authorised Vehicle, P.",
    "Loading & Asccess, F1+F2.", "Local/Water Authority, C.",
    "Goods Vehicles, S.", "Highway Vehicle, X."
])

# Session state init
for key in ["ulev_list", "current_vehicle", "current_vrm", "show_modal", "toggle"]:
    if key not in st.session_state:
        st.session_state[key] = [] if "list" in key else False if "toggle" in key else ""

# Functions
def get_co2_emission(vrm, api_key, url):
    try:
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        response = requests.post(url, json={"registrationNumber": vrm}, headers=headers)
        if response.status_code == 200:
            v = response.json()
            return [{
                "make": v.get("make", "Unknown"),
                "colour": v.get("colour", "Unknown"),
                "emission": v.get("co2Emissions", "Unknown"),
                "type": v.get("typeApproval", "Unknown"),
                "fuel": v.get("fuelType", "Unknown")
            }]
        else:
            st.error(f"Request failed with status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return None

def classify_vehicle_type(type_approval):
    try:
        if type_approval in ["M2", "M3"]:
            return "Bus"
        elif type_approval in ["N1", "N2", "N3"]:
            return "Goods Vehicle"
        elif type_approval == "M1":
            return "Private Car"
        elif type_approval.startswith("L"):
            return "Motorcycle / Trike"
        elif type_approval.startswith("O"):
            return "Trailer"
        else:
            return "Other / Unknown"
    except:
        return "Unknown"

def add_vrm_to_list(exemption_type, vrm):
    vrm_lower = vrm.lower()
    if vrm_lower not in [(v.lower()) for et, v in st.session_state.ulev_list]:
        st.session_state.ulev_list.append((exemption_type, vrm))
        st.success(f"Vehicle Added to the list")
    else:
        st.info("This vehicle is already added.")



# UI - Start
st.title("Enter the registration number of the vehicle")
st.subheader("Registration number (number plate)")
st.text("For example, CU57ABC")

ulev_session = st.checkbox("Check this box if you're processing only ULEVs for a faster experience.")
VRM = st.text_area("", height=70, max_chars=10).strip().upper()



if st.button("Continue"):
    if not VRM:
        st.warning("Please enter a valid registration number.")
    else:
        data = get_co2_emission(VRM, API_KEY, API_URL)
        if data:
            st.session_state.current_vehicle = data[0]
            st.session_state.current_vrm = VRM
            # st.session_state.toggle = True
        else:
            st.warning("No valid data returned.")
            st.session_state.current_vehicle = None
            st.session_state.current_vrm = ""

# UI - Vehicle Info
info = st.session_state.current_vehicle
if info:
    vehicle_type_class = classify_vehicle_type(info['type'])
    try:
        emission_num = int(info['emission'])
    except ValueError:
        st.error(f"Invalid CO2 emission value: {info['emission']}")
        emission_num = None

    # Logic block
    if not ulev_session:
        if st.button("Add VRM to list"):
            if VRM:
                st.session_state.show_modal = True
            else:
                st.warning("Please enter a valid registration number and click Continue.")

        if st.session_state.show_modal:
            exemption_type = st.selectbox("Select vehicle type", EXEMPTION_LIST)
            if st.button("Confirm"):
                current_vrm = st.session_state.current_vrm
                if not current_vrm:
                    st.warning("No VRM selected.")
                else:
                    add_vrm_to_list(exemption_type, current_vrm)
                    st.session_state.show_modal = False
                    st.session_state.current_vehicle = None
                    st.session_state.current_vrm = ""
                    time.sleep(2)
                    st.rerun()


    elif emission_num is not None:
        if emission_num < 74:
            if emission_num == 0 and info['fuel'] == "DIESEL":
                st.markdown("<h1 style='color: red;'>NOT ULEV</h1>", unsafe_allow_html=True)
            else:
                st.markdown("<h1 style='color: green;'>ULEV</h1>", unsafe_allow_html=True)
                if st.button("Add"):
                    add_vrm_to_list("ULEV. U.", st.session_state.current_vrm)
        else:
            st.markdown("<h1 style='color: red;'>NOT ULEV</h1>", unsafe_allow_html=True)

    # Display Info
    st.divider()
    col1, col2 = st.columns([2, 1])  # Adjust ratio as needed
    with col1:
        st.subheader(f"Make: {info['make']}")
        st.subheader(f"Colour: {info['colour']}")
        st.subheader(f"CO2 Emissions: {info['emission']}g/km")
        st.subheader(f"Fuel Type: {info['fuel']}")
        st.subheader(f"Type Approval: {info['type']} ({vehicle_type_class})")
        
    # with col2:
    #     image_url = get_image(st.session_state.current_vrm)
    #     if image_url:
    #         st.image(image_url, caption=f"{info['make']} {st.session_state.current_vrm}", use_container_width=True)
     


# Stored VRMs
if st.session_state.ulev_list:
    st.divider()
    st.write(f"### Stored Vehicles - {len(st.session_state.ulev_list)}")
    for etype, vrm in st.session_state.ulev_list:
        st.write(f"{etype}: {vrm}")

    df_ulevs = pd.DataFrame(st.session_state.ulev_list, columns=["Exemption", "VRM"])
    csv_data = df_ulevs.to_csv(index=False).encode('utf-8')

    if len(st.session_state.ulev_list) > 1:
        st.download_button(
            label="Download ULEV VRMs as CSV",
            data=csv_data,
            file_name="ulev_vrms.csv",
            mime="text/csv"
        )
