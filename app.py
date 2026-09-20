```python
import streamlit as st
import pandas as pd
from math import radians, sin, cos, sqrt, atan2
from itertools import combinations

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="GridPoint",
    page_icon="📍",
    layout="wide"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown("""
<style>

    .main-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 1.15rem;
        color: #6b7280;
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }

    .metric-card {
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        background-color: #ffffff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        text-align: center;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #6b7280;
        margin-bottom: 0.4rem;
    }

    .metric-value {
        font-size: 1.7rem;
        font-weight: 750;
    }

    .result-box {
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #dbeafe;
        background-color: #eff6ff;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    .warehouse-box {
        padding: 0.9rem 1rem;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        margin-bottom: 0.6rem;
        background-color: #fafafa;
    }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DISTANCE FUNCTION
# ---------------------------------------------------------

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
        + cos(lat1)
        * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return R * c


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
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">📍 GRIDPOINT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Warehouse Location Optimization Platform'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Optimize warehouse placement using geographic location "
    "and neighborhood demand to minimize order-weighted "
    "delivery distance."
)

st.divider()

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚙️ Configuration")

    mode = st.radio(
        "Data Mode",
        ["Demo Mode", "Manual Mode"]
    )

    st.divider()

    if mode == "Demo Mode":

        st.success(
            "25 neighborhoods loaded"
        )

        st.info(
            "3 warehouse locations are available "
            "for optimization."
        )

    else:

        st.write(
            "Enter your own neighborhood and warehouse data."
        )

# ---------------------------------------------------------
# DATA
# ---------------------------------------------------------

if mode == "Demo Mode":

    neighborhoods = demo_neighborhoods

    locations = [
        warehouse["name"]
        for warehouse in demo_warehouses
    ]

    coordinates = [
        (
            warehouse["latitude"],
            warehouse["longitude"]
        )
        for warehouse in demo_warehouses
    ]

    num_neighborhoods = len(neighborhoods)
    num_warehouses = len(demo_warehouses)

    st.success(
        "Demo dataset loaded — Bengaluru delivery network"
    )

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    total_orders = sum(
        neighborhood["orders"]
        for neighborhood in neighborhoods
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    Neighborhoods
                </div>
                <div class="metric-value">
                    {num_neighborhoods}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    Warehouses
                </div>
                <div class="metric-value">
                    {num_warehouses}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    Daily Orders
                </div>
                <div class="metric-value">
                    {total_orders:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # NEIGHBORHOOD DATA
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🏘️ Neighborhood Demand'
        '</div>',
        unsafe_allow_html=True
    )

    neighborhood_table = pd.DataFrame(
        neighborhoods
    )

    neighborhood_table.columns = [
        "Neighborhood",
        "Latitude",
        "Longitude",
        "Daily Orders"
    ]

    neighborhood_table["Latitude"] = (
        neighborhood_table["Latitude"].round(4)
    )

    neighborhood_table["Longitude"] = (
        neighborhood_table["Longitude"].round(4)
    )

    st.dataframe(
        neighborhood_table,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------------------------------
    # WAREHOUSE DATA
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🏭 Existing Warehouse Locations'
        '</div>',
        unsafe_allow_html=True
    )

    warehouse_table = pd.DataFrame(
        [
            {
                "Warehouse": i + 1,
                "Location": warehouse["name"],
                "Latitude": warehouse["latitude"],
                "Longitude": warehouse["longitude"]
            }

            for i, warehouse
            in enumerate(demo_warehouses)
        ]
    )

    st.dataframe(
        warehouse_table,
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------------
# MANUAL MODE
# ---------------------------------------------------------

else:

    st.markdown(
        '<div class="section-title">'
        '🏘️ Neighborhood Data'
        '</div>',
        unsafe_allow_html=True
    )

    num_neighborhoods = st.number_input(
        "Number of neighborhoods",
        min_value=1,
        step=1
    )

    neighborhoods = []

    for i in range(
        int(num_neighborhoods)
    ):

        with st.expander(
            f"Neighborhood {i + 1}"
        ):

            neighborhood_name = st.text_input(
                f"Name of Neighborhood {i + 1}"
            )

            neighborhood_latitude = st.number_input(
                f"Latitude {i + 1}",
                format="%.6f"
            )

            neighborhood_longitude = st.number_input(
                f"Longitude {i + 1}",
                format="%.6f"
            )

            daily_orders = st.number_input(
                f"Daily Orders {i + 1}",
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

    st.markdown(
        '<div class="section-title">'
        '🏭 Warehouse Configuration'
        '</div>',
        unsafe_allow_html=True
    )

    num_warehouses = st.number_input(
        "Number of warehouses",
        min_value=1,
        step=1
    )

    locations = []
    coordinates = []

    for i in range(
        int(num_warehouses)
    ):

        with st.expander(
            f"Warehouse {i + 1}"
        ):

            location = st.text_input(
                f"Location of Warehouse {i + 1}"
            )

            latitude = st.number_input(
                f"Latitude of Warehouse {i + 1}",
                format="%.6f"
            )

            longitude = st.number_input(
                f"Longitude of Warehouse {i + 1}",
                format="%.6f"
            )

            locations.append(location)

            coordinates.append(
                (
                    latitude,
                    longitude
                )
            )

# ---------------------------------------------------------
# OPTIMIZE BUTTON
# ---------------------------------------------------------

st.divider()

optimize = st.button(
    "🚀 Optimize Warehouse Locations",
    use_container_width=True,
    type="primary"
)

if optimize:

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

    if not valid_data:

        st.error(
            "Please enter valid details for all warehouses."
        )

    else:

        # -------------------------------------------------
        # CURRENT ASSIGNMENTS
        # -------------------------------------------------

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
                    "Neighborhood":
                        neighborhood["name"],

                    "Orders":
                        neighborhood["orders"],

                    "Assigned Warehouse":
                        nearest_warehouse,

                    "Distance (km)":
                        nearest_distance
                }
            )

        # -------------------------------------------------
        # CURRENT COST
        # -------------------------------------------------

        current_cost = sum(
            assignment["Distance (km)"]
            * assignment["Orders"]

            for assignment in assignments
        )

        # -------------------------------------------------
        # OPTIMIZATION
        # -------------------------------------------------

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
        # RESULTS HEADER
        # -------------------------------------------------

        st.divider()

        st.markdown(
            '<div class="section-title">'
            '🎯 Optimization Results'
            '</div>',
            unsafe_allow_html=True
        )

        st.success(
            "GridPoint successfully identified "
            "the optimal warehouse location(s)."
        )

        # -------------------------------------------------
        # RESULT METRICS
        # -------------------------------------------------

        savings = current_cost - best_cost

        if current_cost > 0:

            savings_percentage = (
                savings / current_cost
            ) * 100

        else:

            savings_percentage = 0

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">
                        Current Distance
                    </div>
                    <div class="metric-value">
                        {current_cost:,.0f}
                    </div>
                    <div class="metric-label">
                        order-km
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">
                        Optimized Distance
                    </div>
                    <div class="metric-value">
                        {best_cost:,.0f}
                    </div>
                    <div class="metric-label">
                        order-km
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">
                        Distance Reduction
                    </div>
                    <div class="metric-value">
                        {savings:,.0f}
                    </div>
                    <div class="metric-label">
                        order-km
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">
                        Percentage Reduction
                    </div>
                    <div class="metric-value">
                        {savings_percentage:.1f}%
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # -------------------------------------------------
        # RECOMMENDED LOCATIONS
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '📍 Recommended Warehouse Locations'
            '</div>',
            unsafe_allow_html=True
        )

        for warehouse in best_combination:

            st.markdown(
                f"""
                <div class="warehouse-box">
                    <strong>📦 {warehouse["name"]}</strong><br>
                    Latitude: {warehouse["latitude"]:.4f}
                    &nbsp;&nbsp;|&nbsp;&nbsp;
                    Longitude: {warehouse["longitude"]:.4f}
                </div>
                """,
                unsafe_allow_html=True
            )

        # -------------------------------------------------
        # OPTIMIZED ASSIGNMENTS
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '🔗 Optimized Neighborhood Assignments'
            '</div>',
            unsafe_allow_html=True
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
                    "Neighborhood":
                        neighborhood["name"],

                    "Orders":
                        neighborhood["orders"],

                    "Assigned Warehouse":
                        nearest_warehouse,

                    "Distance (km)":
                        round(
                            nearest_distance,
                            2
                        )
                }
            )

        st.dataframe(
            optimized_assignments,
            use_container_width=True,
            hide_index=True
        )

        # -------------------------------------------------
        # MAP
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '🗺️ Optimized Network Map'
            '</div>',
            unsafe_allow_html=True
        )

        map_data = pd.DataFrame(
            [
                {
                    "latitude":
                        neighborhood["latitude"],

                    "longitude":
                        neighborhood["longitude"]
                }

                for neighborhood in neighborhoods
            ]
            +
            [
                {
                    "latitude":
                        warehouse["latitude"],

                    "longitude":
                        warehouse["longitude"]
                }

                for warehouse in best_combination
            ]
        )

        st.map(
            map_data,
            use_container_width=True
        )

        # -------------------------------------------------
        # EXPLANATION
        # -------------------------------------------------

        st.info(
            "GridPoint uses a discrete K-Median-style "
            "optimization approach. It evaluates candidate "
            "warehouse combinations and minimizes total "
            "order-weighted Haversine delivery distance."
        )
```

**Do this now:** replace `app.py` → save → run it locally → choose **Demo Mode** → click **Optimize Warehouse Locations**.

If it runs correctly, **do not make any more UI changes**. Commit + push it, and Streamlit Cloud should redeploy.
