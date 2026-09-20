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

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


st.title("📍 GRIDPOINT")
st.subheader("Warehouse Location Optimization Platform")

st.write(
    "GridPoint uses neighborhood demand and geographic locations "
    "to identify warehouse locations that minimize order-weighted "
    "delivery distance."
)

# ---------------------------------------------------------
# DEMO / MANUAL MODE
# ---------------------------------------------------------

mode = st.selectbox(
    "Choose Mode",
    ["Demo Mode", "Manual Mode"]
)

# ---------------------------------------------------------
# DEMO DATA
# ---------------------------------------------------------

demo_neighborhoods = [
    {"name": "Koramangala", "latitude": 12.9352, "longitude": 77.6245, "orders": 120},
    {"name": "Indiranagar", "latitude": 12.9784, "longitude": 77.6408, "orders": 95},
    {"name": "Whitefield", "latitude": 12.9698, "longitude": 77.7500, "orders": 150},
    {"name": "Yeshwanthpur", "latitude": 13.0285, "longitude": 77.5548, "orders": 70},
    {"name": "Jayanagar", "latitude": 12.9250, "longitude": 77.5938, "orders": 100},
    {"name": "HSR Layout", "latitude": 12.9138, "longitude": 77.6649, "orders": 110},
    {"name": "Mahadevapura", "latitude": 12.9904, "longitude": 77.6842, "orders": 140},
    {"name": "Malleswaram", "latitude": 13.0081, "longitude": 77.5648, "orders": 75},
    {"name": "Marathahalli", "latitude": 12.9591, "longitude": 77.6974, "orders": 135},
    {"name": "Electronic City", "latitude": 12.8452, "longitude": 77.6602, "orders": 160},
    {"name": "Banashankari", "latitude": 12.9255, "longitude": 77.5468, "orders": 85},
    {"name": "Rajajinagar", "latitude": 12.9910, "longitude": 77.5540, "orders": 90},
    {"name": "Bellandur", "latitude": 12.9304, "longitude": 77.6784, "orders": 145},
    {"name": "Hebbal", "latitude": 13.0358, "longitude": 77.5970, "orders": 105},
    {"name": "BTM Layout", "latitude": 12.9166, "longitude": 77.6101, "orders": 115},
    {"name": "JP Nagar", "latitude": 12.9063, "longitude": 77.5857, "orders": 95},
    {"name": "Kengeri", "latitude": 12.9141, "longitude": 77.4828, "orders": 60},
    {"name": "RT Nagar", "latitude": 13.0196, "longitude": 77.5946, "orders": 65},
    {"name": "Cox Town", "latitude": 13.0005, "longitude": 77.6163, "orders": 55},
    {"name": "Domlur", "latitude": 12.9609, "longitude": 77.6387, "orders": 80},
    {"name": "Ulsoor", "latitude": 12.9817, "longitude": 77.6198, "orders": 70},
    {"name": "Vijayanagar", "latitude": 12.9719, "longitude": 77.5299, "orders": 85},
    {"name": "Nagarbhavi", "latitude": 12.9591, "longitude": 77.5122, "orders": 65},
    {"name": "KR Puram", "latitude": 13.0072, "longitude": 77.6954, "orders": 125},
    {"name": "Yelahanka", "latitude": 13.1007, "longitude": 77.5963, "orders": 90}
]

demo_warehouses = [
    {
        "name": "Yeshwanthpur Warehouse",
        "latitude": 13.0285,
        "longitude": 77.5548
    },
    {
        "name": "Whitefield Warehouse",
        "latitude": 12.9698,
        "longitude": 77.7500
    },
    {
        "name": "Electronic City Warehouse",
        "latitude": 12.8452,
        "longitude": 77.6602
    }
]

# ---------------------------------------------------------
# DEMO MODE
# ---------------------------------------------------------

if mode == "Demo Mode":

    neighborhoods = demo_neighborhoods
    locations = [
        warehouse["name"] for warehouse in demo_warehouses
    ]
    coordinates = [
        (warehouse["latitude"], warehouse["longitude"])
        for warehouse in demo_warehouses
    ]

    num_neighborhoods = len(neighborhoods)
    num_warehouses = len(demo_warehouses)

    st.success(
        "Demo dataset loaded: 25 Bengaluru neighborhoods and 3 warehouses."
    )

    st.header("Neighborhood Data")

    neighborhood_table = pd.DataFrame(neighborhoods)

    neighborhood_table.columns = [
        "Neighborhood",
        "Latitude",
        "Longitude",
        "Daily Orders"
    ]

    st.dataframe(
        neighborhood_table,
        use_container_width=True
    )

    st.header("Warehouse Data")

    warehouse_table = pd.DataFrame(
        [
            {
                "Warehouse": i + 1,
                "Location": warehouse["name"],
                "Latitude": warehouse["latitude"],
                "Longitude": warehouse["longitude"]
            }
            for i, warehouse in enumerate(demo_warehouses)
        ]
    )

    st.dataframe(
        warehouse_table,
        use_container_width=True
    )

# ---------------------------------------------------------
# MANUAL MODE
# ---------------------------------------------------------

else:

    st.header("Neighborhood Data")

    st.write(
        "Enter the neighborhoods, their locations, and daily order demand."
    )

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
            f"Latitude of Neighborhood {i + 1}",
            format="%.6f"
        )

        neighborhood_longitude = st.number_input(
            f"Longitude of Neighborhood {i + 1}",
            format="%.6f"
        )

        daily_orders = st.number_input(
            f"Daily Orders in Neighborhood {i + 1}",
            min_value=0,
            step=1
        )

        neighborhoods.append(
            {
                "name": neighborhood_name,
                "latitude": neighborhood_latitude,
                "longitude": neighborhood_longitude,
                "orders": daily_orders
            }
        )

    st.header("Optimization Settings")

    st.write(
        "Choose the number of warehouses GridPoint should determine."
    )

    num_warehouses = st.number_input(
        "Number of warehouses",
        min_value=1,
        step=1
    )

    st.write("Enter the warehouse coordinates below:")

    locations = []
    coordinates = []

    for i in range(int(num_warehouses)):

        st.subheader(f"Warehouse {i + 1}")

        location = st.text_input(
            f"Location of Warehouse {i + 1}"
        )

        locations.append(location)

        latitude = st.number_input(
            f"Latitude of Warehouse {i + 1}",
            format="%.6f"
        )

        longitude = st.number_input(
            f"Longitude of Warehouse {i + 1}",
            format="%.6f"
        )

        coordinates.append(
            (latitude, longitude)
        )


# ---------------------------------------------------------
# OPTIMIZATION
# ---------------------------------------------------------

if st.button("🚀 Optimize Warehouses"):

    if mode == "Demo Mode":

        valid_data = True

    else:

        valid_data = (
            all(locations)
            and all(
                lat != 0 and lon != 0
                for lat, lon in coordinates
            )
        )

    if valid_data:

        st.success("Warehouse data accepted!")

        # -------------------------------------------------
        # WAREHOUSE DETAILS
        # -------------------------------------------------

        st.subheader("Warehouse Details")

        data = []

        for i in range(int(num_warehouses)):

            data.append(
                {
                    "Warehouse": i + 1,
                    "Location": locations[i],
                    "Latitude": coordinates[i][0],
                    "Longitude": coordinates[i][1]
                }
            )

        st.dataframe(
            data,
            use_container_width=True
        )

        # -------------------------------------------------
        # WAREHOUSE DISTANCES
        # -------------------------------------------------

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
                    f"Distance between Warehouse {i + 1} "
                    f"and Warehouse {j + 1}: "
                    f"{distance:.2f} km"
                )

        # -------------------------------------------------
        # CURRENT ASSIGNMENTS
        # -------------------------------------------------

        st.subheader("Neighborhood Assignments")

        assignments = []

        for neighborhood in neighborhoods:

            nearest_warehouse = None
            nearest_distance = float("inf")

            for i, (
                warehouse_lat,
                warehouse_lon
            ) in enumerate(coordinates):

                distance = calculate_distance(
                    neighborhood["latitude"],
                    neighborhood["longitude"],
                    warehouse_lat,
                    warehouse_lon
                )

                if distance < nearest_distance:

                    nearest_distance = distance
                    nearest_warehouse = i + 1

            assignments.append(
                {
                    "Neighborhood": neighborhood["name"],
                    "Orders": neighborhood["orders"],
                    "Assigned Warehouse": nearest_warehouse,
                    "Distance (km)": nearest_distance
                }
            )

        st.dataframe(
            pd.DataFrame(assignments).assign(
                **{
                    "Distance (km)": lambda x:
                    x["Distance (km)"].round(2)
                }
            ),
            use_container_width=True
        )

        # -------------------------------------------------
        # CURRENT COST
        # -------------------------------------------------

        st.subheader("📦 Current Weighted Delivery Distance")

        total_weighted_distance = 0

        for assignment in assignments:

            weighted_distance = (
                assignment["Distance (km)"]
                * assignment["Orders"]
            )

            total_weighted_distance += weighted_distance

        st.write(
            f"{total_weighted_distance:.2f} order-km"
        )

        # -------------------------------------------------
        # OPTIMIZATION
        # -------------------------------------------------

        st.subheader("🎯 GridPoint Optimization Result")

        candidate_locations = neighborhoods

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

                total_cost += (
                    nearest_distance
                    * neighborhood["orders"]
                )

            if total_cost < best_cost:

                best_cost = total_cost
                best_combination = combination

        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        st.success(
            "GridPoint found the optimal warehouse location(s)!"
        )

        st.write(
            "Recommended Warehouse Location(s):"
        )

        for warehouse in best_combination:

            st.write(
                f"📍 {warehouse['name']} "
                f"({warehouse['latitude']}, "
                f"{warehouse['longitude']})"
            )

        st.write(
            f"Optimized Weighted Delivery Distance: "
            f"{best_cost:.2f} order-km"
        )

        # -------------------------------------------------
        # OPTIMIZED ASSIGNMENTS
        # -------------------------------------------------

        st.subheader(
            "Optimized Neighborhood Assignments"
        )

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

            optimized_assignments.append(
                {
                    "Neighborhood": neighborhood["name"],
                    "Orders": neighborhood["orders"],
                    "Assigned Warehouse": nearest_warehouse,
                    "Distance (km)": round(
                        nearest_distance,
                        2
                    )
                }
            )

        st.dataframe(
            optimized_assignments,
            use_container_width=True
        )

        # -------------------------------------------------
        # COST COMPARISON
        # -------------------------------------------------

        current_cost = total_weighted_distance
        optimized_cost = best_cost

        savings = current_cost - optimized_cost

        if current_cost > 0:

            savings_percentage = (
                savings / current_cost
            ) * 100

        else:

            savings_percentage = 0

        st.subheader("💰 Delivery Cost Comparison")

        st.write(
            f"Current Weighted Delivery Distance: "
            f"{current_cost:.2f} order-km"
        )

        st.write(
            f"Optimized Weighted Delivery Distance: "
            f"{optimized_cost:.2f} order-km"
        )

        st.write(
            f"Delivery Distance Reduction: "
            f"{savings:.2f} order-km"
        )

        st.write(
            f"Percentage Reduction: "
            f"{savings_percentage:.2f}%"
        )

        # -------------------------------------------------
        # MAP
        # -------------------------------------------------

        map_data = pd.DataFrame(
            [
                {
                    "latitude": neighborhood["latitude"],
                    "longitude": neighborhood["longitude"]
                }
                for neighborhood in neighborhoods
            ]
            +
            [
                {
                    "latitude": warehouse["latitude"],
                    "longitude": warehouse["longitude"]
                }
                for warehouse in best_combination
            ]
        )

        st.subheader(
            "🗺️ Optimized Warehouse & Neighborhood Map"
        )

        st.map(map_data)

        st.info(
            "GridPoint recommends warehouse location(s) "
            "that minimize order-weighted delivery distance."
        )

    else:

        st.error(
            "Please enter valid details for all warehouses."
        )