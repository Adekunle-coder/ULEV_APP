# ULEV_APP
This is a Streamlit web application that allows users to:

Enter a UK vehicle registration number (VRM)

Retrieve CO₂ emission data and vehicle details via the UK DVLA API

Automatically classify the vehicle as ULEV (Ultra Low Emission Vehicle) or not

View vehicle make, color, emission level, and type approval

Store and download a list of ULEV vehicles as a CSV file

# Features
Input VRM and fetch real-time vehicle data from the DVLA Vehicle Enquiry API

Automatic classification based on CO₂ emissions

Visual feedback indicating whether a vehicle qualifies as ULEV (emissions < 74 g/km)

Type approval classification (e.g., Private Car, Bus, Goods Vehicle)

Downloadable list of identified ULEV VRMs as a CSV

# Tech Stack

Python 3

Streamlit – UI framework

Requests – For API calls

Pandas – For handling tabular data and CSV export
