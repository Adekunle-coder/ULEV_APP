import requests
import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


def get_co2_emission(vrm, api_key, url):
    
    data = []
    try:
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        input_vrm = {"registrationNumber": vrm}
        response = requests.post(url, json=input_vrm, headers=headers)

        if response.status_code == 200:
            vehicle_data = response.json()
            make = vehicle_data.get('make', 'Unknown')
            colour = vehicle_data.get('colour', 'Unknown')
            emission = vehicle_data.get('co2Emissions', 'Unknown')
            vehicle_type = vehicle_data.get('typeApproval', 'Unknown')
            fuelType = vehicle_data.get('fuelType', 'Unknown')


            data.append({
                "make": make,
                "colour": colour,
                "emission": emission,
                "type": vehicle_type,
                "fuel": fuelType
            })
            return data
        else:
            st.write(f"Request failed with status code {response.status_code}")
            return None
    except Exception as e:
        st.write("Error occurred:", e)
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
    except Exception as e:
        st.write("Error classifying vehicle type:", e)
        return "Unknown"

# Initialize session state variables if not present
if "ulev_list" not in st.session_state:
    st.session_state.ulev_list = []
if "current_vehicle" not in st.session_state:
    st.session_state.current_vehicle = None
if "current_vrm" not in st.session_state:
    st.session_state.current_vrm = ""

st.title("Enter the registration number of the vehicle")
st.subheader("Registration number (number plate)")
st.text("For example, CU57ABC")
VRM = st.text_area("", height=70, max_chars=10)

if st.button("Continue"):
    if not VRM.strip():
        st.warning("Please enter a valid registration number.")
    else:
        url = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"
        API_KEY = os.getenv("API_KEY")
        data = get_co2_emission(VRM.strip(), API_KEY, url)
        if data and isinstance(data, list):
            st.session_state.current_vehicle = data[0]
            st.session_state.current_vrm = VRM.strip()
        else:
            st.warning("No valid data returned. Please check the registration number and try again.")
            st.session_state.current_vehicle = None
            st.session_state.current_vrm = ""

# Now display the vehicle info if present in session state
if st.session_state.current_vehicle:
    info = st.session_state.current_vehicle
    emission_value = info['emission']
    fuel_type = info['fuel']

    vehicle_type = info['type']
    vehicle_type_class = classify_vehicle_type(vehicle_type)

    try:
        emission_num = int(emission_value)
        if emission_num < 74 and fuel_type != "DIESEL":
            st.markdown("<h1 style='color: green;'>ULEV</h1>", unsafe_allow_html=True)
            if st.button("Add"):
                if st.session_state.current_vrm not in st.session_state.ulev_list:
                    st.session_state.ulev_list.append(st.session_state.current_vrm)
                else:
                    st.info("This VRM is already added.")
        else:
            st.markdown("<h1 style='color: red;'>NOT ULEV</h1>", unsafe_allow_html=True)
    except ValueError:
        st.write("Emission value is not a valid number:", emission_value)

    st.divider()

    st.subheader(f"Make: {info['make']}")
    st.subheader(f"Colour: {info['colour']}")
    st.subheader(f"CO2 Emissions: {emission_value}g/km")
    st.subheader(f"Fuel Type: {fuel_type}")
    st.subheader(f"Type Approval: {vehicle_type} ({vehicle_type_class})")

    st.divider()

if st.session_state.ulev_list:
    st.write("### Stored ULEV Vehicles")
    for vrm in st.session_state.ulev_list:
        st.write(f"- {vrm}")

df_ulevs = pd.DataFrame(st.session_state.ulev_list, columns=["VRM"])

csv_data = df_ulevs.to_csv(index=False).encode('utf-8')
    
if len(st.session_state.ulev_list) > 1:
    st.download_button(
        label="Download ULEV VRMs as CSV",
        data=csv_data,
        file_name="ulev_vrms.csv",
        mime="text/csv"
    )
