import requests
import streamlit as st


def get_co2_emission(vrm, api_key, url):
    data = []
    
    try:
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }
        input_vrm = {
            "registrationNumber": vrm
        }

        response = requests.post(url, json=input_vrm, headers=headers)

        if response.status_code == 200:
            try:
                vehicle_data = response.json()
                make = vehicle_data.get('make', 'Unknown')
                colour = vehicle_data.get('colour', 'Unknown')
                emission = vehicle_data.get('co2Emissions', 'Unknown')
                vehicle_type = vehicle_data.get('typeApproval', 'Unknown')

                data.append({
                    "make": make,
                    "colour": colour,
                    "emission": emission,
                    "type": vehicle_type
                })
                return data
            except Exception as json_error:
                st.write("Error processing JSON response:")
                st.write(json_error)
                return None
        else:
            st.write(f"Request failed with status code {response.status_code}")
            return None

    except requests.exceptions.RequestException as req_error:
        st.write("Request exception occurred:")
        st.write(req_error)
        return None
    except Exception as general_error:
        st.write("An unexpected error occurred:")
        st.write(general_error)
        return None


def classify_vehicle_type(type_approval):
    try:
        if type_approval in ["M2", "M3"]:
            return "Bus"
        elif type_approval in ["N1", "N2", "N3"]:
            return "Goods Vehicle"
        elif type_approval == "M1":
            return "Passenger Car"
        elif type_approval.startswith("L"):
            return "Motorcycle / Trike"
        elif type_approval.startswith("O"):
            return "Trailer"
        else:
            return "Other / Unknown"
    except Exception as e:
        st.write("Error classifying vehicle type:", e)
        return "Unknown"


st.title("Enter the registration number of the vehicle")
st.subheader("Registration number (number plate)")
st.text("For example, CU57ABC")
VRM = st.text_area("", height=70, max_chars=10)

if st.button("Continue"):
    if not VRM.strip():
        st.warning("Please enter a valid registration number.")
    else:
        try:
            url = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"
            API_KEY = "g3iPHWSLfm2yd9bBzy8C25GEZ8r276Ha9ekLTLsQ"
            result = get_co2_emission(VRM.strip(), API_KEY, url)

            

            if result and isinstance(result, list):
                info = result[0]
                emission_value = info['emission']
                vehicle_type = info['type']
                vehicle_type_class = classify_vehicle_type(vehicle_type)

                try:
                    emission_num = int(emission_value)
                    if emission_num < 74:
                        st.markdown("<h1 style='color: green;'>ULEV</h1>", unsafe_allow_html=True)
                    else:
                        st.markdown("<h1 style='color: red;'>NOT ULEV</h1>", unsafe_allow_html=True)
                except ValueError:
                    st.write("Emission value is not a valid number:", emission_value)
                
                st.divider()

                st.subheader(f"Make: {info['make']}")
                st.subheader(f"Colour: {info['colour']}")
                st.subheader(f"CO2 Emissions: {emission_value}g/km")
                st.subheader(f"Type Approval: {vehicle_type} ({vehicle_type_class})")
                # Check and display ULEV status

            else:
                st.warning("No valid data returned. Please check the registration number and try again.")

        except Exception as final_error:
            st.write("An error occurred during processing:")
            st.write(final_error)
