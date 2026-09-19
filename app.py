import streamlit as st
import pandas as pd

st.title("GRIDPOINT")
st.write("Warehouse Location Optimization Platform")

st.header("Warehouse Data")

num_warehouses = st.number_input("Number of warehouses", min_value=1, step=1)

st.write("Enter the warehouse coordinates below:")

locations = []
coordinates = []

for i in range(int(num_warehouses)):
    st.subheader(f"Warehouse {i + 1}")
    location = st.text_input(f"Location of Warehouse {i + 1}")
    locations.append(location)
    latitude = st.number_input(f"Latitude of Warehouse {i + 1}")
    longitude = st.number_input(f"Longitude of Warehouse {i + 1}")
    coordinates.append((latitude, longitude))

if st.button("Optimize Warehouses"):
    if all(locations) and all(lat != 0 and lon != 0 for lat, lon in coordinates):
        st.success("Optimization started!")
    else:
        st.error("Please enter valid details for all warehouses.")




















