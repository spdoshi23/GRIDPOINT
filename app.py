import streamlit as st
import pandas as pd
from math import radians, sin, cos, sqrt, atan2
from itertools import combinations

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

st.title("📍 GRIDPOINT")
st.subheader("Warehouse Location Optimization Platform")

st.write(
    "GridPoint uses neighborhood demand and geographic locations "
    "to identify warehouse locations that minimize order-weighted "
    "delivery distance."
)

st.header("Neighborhood Data")
st.write("Enter the neighborhoods, their locations, and daily order demand.")

num_neighborhoods = st.number_input(
    "Number of neighborhoods",
    min_value=1,
    step=1
)

neighborhoods = []

for i in range(int(num_neighborhoods)):
    st.subheader(f"Neighborhood {i + 1}")

    neighborhood_name = st.text_input(
        f"Name of Neighborhood {i + 1}"
    )

    neighborhood_latitude = st.number_input(
        f"Latitude of Neighborhood {i + 1}"
    )

    neighborhood_longitude = st.number_input(
        f"Longitude of Neighborhood {i + 1}"
    )

    daily_orders = st.number_input(
        f"Daily Orders in Neighborhood {i + 1}",
        min_value=0,
        step=1
    )

    neighborhoods.append({
        "name": neighborhood_name,
        "latitude": neighborhood_latitude,
        "longitude": neighborhood_longitude,
        "orders": daily_orders
    })

st.header("Optimization Settings")

st.write(
    "Choose the optimization objective and number of warehouses "
    "GridPoint should determine."
)

objective = st.selectbox(
    "What should GridPoint optimize?",
    ["Minimize total distance"]
)

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
        st.success("Warehouse data accepted!")
        st.write("Warehouse Details")

        data = []

        for i in range(int(num_warehouses)):
            data.append({
                "Warehouse": i + 1,
                "Location": locations[i],
                "Latitude": coordinates[i][0],
                "Longitude": coordinates[i][1]
            })

        st.dataframe(data)

        st.subheader("Distances Between Warehouses")

        for i in range(len(coordinates)):
            for j in range(i + 1, len(coordinates)):
                distance = calculate_distance(
                    coordinates[i][0],
                    coordinates[i][1],
                    coordinates[j][0],
                    coordinates[j][1]
                )

                st.write(
                    f"Distance between Warehouse {i + 1} and Warehouse {j + 1}: "
                    f"{distance:.2f} km"
                )

        st.subheader("Neighborhood Assignments")

        assignments = []

        for neighborhood in neighborhoods:
            nearest_warehouse = None
            nearest_distance = float("inf")

            for i, (warehouse_lat, warehouse_lon) in enumerate(coordinates):
                distance = calculate_distance(
                    neighborhood["latitude"],
                    neighborhood["longitude"],
                    warehouse_lat,
                    warehouse_lon
                )

                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_warehouse = i + 1

            assignments.append({
                "Neighborhood": neighborhood["name"],
                "Orders": neighborhood["orders"],
                "Assigned Warehouse": nearest_warehouse,
                "Distance (km)": round(nearest_distance, 2)
                })

        st.dataframe(assignments)

        total_weighted_distance = 0

        for assignment in assignments:
            weighted_distance = (
                assignment["Distance (km)"] * assignment["Orders"]
            )

            total_weighted_distance += weighted_distance

        st.subheader("📦 Current Weighted Delivery Cost")

        st.write(
            f"{total_weighted_distance:.2f} order-km"
        )

        avg_latitude = sum(lat for lat, lon in coordinates) / len(coordinates)
        avg_longitude = sum(lon for lat, lon in coordinates) / len(coordinates)

        st.subheader("🎯 GridPoint Optimization Result")

        candidate_locations = [neighborhood for neighborhood in neighborhoods]

        best_combination = None
        best_cost = float("inf")

        for combination in combinations(
            candidate_locations,
            int(num_warehouses)
        ):
            total_cost = 0

            for neighborhood in neighborhoods:
                nearest_distance = float("inf")

                for warehouse in combination:
                    distance = calculate_distance(
                        neighborhood["latitude"],
                        neighborhood["longitude"],
                        warehouse["latitude"],
                        warehouse["longitude"]
                    )

                    if distance < nearest_distance:
                        nearest_distance = distance

                total_cost += nearest_distance * neighborhood["orders"]

            if total_cost < best_cost:
                best_cost = total_cost
                best_combination = combination

        st.success("GridPoint found the optimal warehouse location(s)!")

        st.write("Recommended Warehouse Location(s):")

        for warehouse in best_combination:
            st.write(
                f"{warehouse['name']} "
                f"({warehouse['latitude']}, {warehouse['longitude']})"
            )

        st.write(
            f"Optimized Weighted Delivery Distance: "
            f"{best_cost:.2f} order-km"
        )

        st.subheader("Optimized Neighborhood Assignments")

        optimized_assignments = []

        for neighborhood in neighborhoods:
            nearest_warehouse = None
            nearest_distance = float("inf")

            for warehouse in best_combination:
                distance = calculate_distance(
                    neighborhood["latitude"],
                    neighborhood["longitude"],
                    warehouse["latitude"],
                    warehouse["longitude"]
                )

                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_warehouse = warehouse["name"]

            optimized_assignments.append({
                "Neighborhood": neighborhood["name"],
                "Orders": neighborhood["orders"],
                "Assigned Warehouse": nearest_warehouse,
                "Distance (km)": round(nearest_distance, 2)
            })

        st.dataframe(optimized_assignments)

        

        current_cost = total_weighted_distance

        optimized_cost = best_cost
        
        savings = current_cost - optimized_cost

        savings_percentage = (savings / current_cost) * 100

        st.subheader("💰 Delivery Cost Comparison")

        st.write(f"Current Weighted Delivery Distance: {current_cost:.2f} order-km")
        st.write(f"Optimized Weighted Delivery Distance: {optimized_cost:.2f} order-km")
        st.write(f"Delivery Distance Reduction: {savings:.2f} order-km")
        st.write(f"Percentage Reduction: {savings_percentage:.2f}%")
        st.info(
            "GridPoint recommends the warehouse location(s) "
            "that minimize order-weighted delivery distance."
        )

        map_data = pd.DataFrame(
            [
                {
                    "latitude": neighborhood["latitude"],
                    "longitude": neighborhood["longitude"],
                    "Type": "Neighborhood"
                }
                for neighborhood in neighborhoods
            ]
            +
            [
                {
        "latitude": warehouse["latitude"],
        "longitude": warehouse["longitude"],
        "Type": "Optimized Warehouse"
                }
                for warehouse in best_combination
            ]
        )

        st.subheader("🗺️ Optimized Warehouse & Neighborhood Map")
        st.map(map_data)
        

    else:
        st.error("Please enter valid details for all warehouses.")






















