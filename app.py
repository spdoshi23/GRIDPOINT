import streamlit as st
import pandas as pd
import pydeck as pdk
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
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 18px;
    opacity: 0.75;
    margin-bottom: 25px;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 12px;
}

.metric-card {
    padding: 18px;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,0.25);
    text-align: center;
}

.metric-value {
    font-size: 28px;
    font-weight: 700;
}

.metric-label {
    font-size: 14px;
    opacity: 0.7;
}

.warehouse-card {
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(34,197,94,0.5);
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("⚙️ GridPoint")

theme = st.sidebar.radio(
    "🎨 Appearance",
    ["Light Mode", "Dark Mode"]
)

mode = st.sidebar.radio(
    "📊 Data Mode",
    ["Demo Mode", "Manual Mode"]
)


# ---------------------------------------------------------
# THEME
# ---------------------------------------------------------

if theme == "Dark Mode":

    st.markdown("""
    <style>

    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    .metric-card {
        background-color: #1e293b;
    }

    .warehouse-card {
        background-color: #13251a;
    }

    </style>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <style>

    .stApp {
        background-color: #ffffff;
        color: #111827;
    }

    .metric-card {
        background-color: #f8fafc;
    }

    .warehouse-card {
        background-color: #f0fdf4;
    }

    </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">📍 GridPoint</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Warehouse Location Optimization Platform</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# DEMO DATA
# ---------------------------------------------------------

demo_neighborhoods = [
    ["Koramangala", 12.9352, 77.6245, 120],
    ["Indiranagar", 12.9784, 77.6408, 95],
    ["Whitefield", 12.9698, 77.7500, 150],
    ["Yeshwanthpur", 13.0285, 77.5548, 70],
    ["Jayanagar", 12.9250, 77.5938, 100],
    ["HSR Layout", 12.9138, 77.6649, 110],
    ["Mahadevapura", 12.9904, 77.6842, 140],
    ["Malleswaram", 13.0081, 77.5648, 75],
    ["Marathahalli", 12.9591, 77.6974, 135],
    ["Electronic City", 12.8452, 77.6602, 160],
    ["Banashankari", 12.9255, 77.5468, 85],
    ["Rajajinagar", 12.9910, 77.5540, 90],
    ["Bellandur", 12.9304, 77.6784, 145],
    ["Hebbal", 13.0358, 77.5970, 105],
    ["BTM Layout", 12.9166, 77.6101, 115],
    ["JP Nagar", 12.9063, 77.5857, 95],
    ["Kengeri", 12.9141, 77.4828, 60],
    ["RT Nagar", 13.0196, 77.5946, 65],
    ["Cox Town", 13.0005, 77.6163, 55],
    ["Domlur", 12.9609, 77.6387, 80],
    ["Ulsoor", 12.9817, 77.6198, 70],
    ["Vijayanagar", 12.9719, 77.5299, 85],
    ["Nagarbhavi", 12.9591, 77.5122, 65],
    ["KR Puram", 13.0072, 77.6954, 125],
    ["Yelahanka", 13.1007, 77.5963, 90]
]

demo_warehouses = [
    ["Yeshwanthpur Warehouse", 13.0285, 77.5548],
    ["Whitefield Warehouse", 12.9698, 77.7500],
    ["Electronic City Warehouse", 12.8452, 77.6602]
]


# ---------------------------------------------------------
# DATA INPUT
# ---------------------------------------------------------

if mode == "Demo Mode":

    neighborhoods = pd.DataFrame(
        demo_neighborhoods,
        columns=["Neighborhood", "Latitude", "Longitude", "Daily Orders"]
    )

    warehouses = pd.DataFrame(
        demo_warehouses,
        columns=["Warehouse", "Latitude", "Longitude"]
    )

else:

    st.markdown(
        '<div class="section-title">🏘️ Neighborhood Data</div>',
        unsafe_allow_html=True
    )

    num_neighborhoods = st.number_input(
        "Number of neighborhoods",
        min_value=2,
        max_value=25,
        value=5,
        step=1
    )

    neighborhood_data = []

    for i in range(num_neighborhoods):

        with st.expander(f"Neighborhood {i + 1}"):

            name = st.text_input(
                "Neighborhood name",
                value=f"Neighborhood {i + 1}",
                key=f"name_{i}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                latitude = st.number_input(
                    "Latitude",
                    value=12.9716,
                    format="%.6f",
                    key=f"lat_{i}"
                )

            with col2:
                longitude = st.number_input(
                    "Longitude",
                    value=77.5946,
                    format="%.6f",
                    key=f"lon_{i}"
                )

            with col3:
                orders = st.number_input(
                    "Daily Orders",
                    min_value=1,
                    value=100,
                    step=1,
                    key=f"orders_{i}"
                )

            neighborhood_data.append(
                [name, latitude, longitude, orders]
            )

    neighborhoods = pd.DataFrame(
        neighborhood_data,
        columns=["Neighborhood", "Latitude", "Longitude", "Daily Orders"]
    )

    st.markdown(
        '<div class="section-title">🏭 Warehouse Data</div>',
        unsafe_allow_html=True
    )

    num_warehouses = st.number_input(
        "Number of warehouses",
        min_value=1,
        max_value=5,
        value=2,
        step=1
    )

    warehouse_data = []

    for i in range(num_warehouses):

        with st.expander(f"Warehouse {i + 1}"):

            name = st.text_input(
                "Warehouse name",
                value=f"Warehouse {i + 1}",
                key=f"warehouse_name_{i}"
            )

            col1, col2 = st.columns(2)

            with col1:
                latitude = st.number_input(
                    "Latitude",
                    value=12.9716,
                    format="%.6f",
                    key=f"warehouse_lat_{i}"
                )

            with col2:
                longitude = st.number_input(
                    "Longitude",
                    value=77.5946,
                    format="%.6f",
                    key=f"warehouse_lon_{i}"
                )

            warehouse_data.append(
                [name, latitude, longitude]
            )

    warehouses = pd.DataFrame(
        warehouse_data,
        columns=["Warehouse", "Latitude", "Longitude"]
    )


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">📊 Network Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{len(neighborhoods)}</div>
            <div class="metric-label">Neighborhoods</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{len(warehouses)}</div>
            <div class="metric-label">Warehouses</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    total_orders = neighborhoods["Daily Orders"].sum()

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{total_orders:,}</div>
            <div class="metric-label">Daily Orders</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# DATA TABLES
# ---------------------------------------------------------

with st.expander("🏘️ View Neighborhood Demand"):

    st.dataframe(
        neighborhoods,
        use_container_width=True,
        hide_index=True
    )


with st.expander("🏭 View Warehouse Locations"):

    st.dataframe(
        warehouses,
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------------
# HAVERSINE DISTANCE
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

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


# ---------------------------------------------------------
# CURRENT ASSIGNMENTS
# ---------------------------------------------------------

def calculate_assignments(neighborhoods, warehouses):

    assignments = []
    total_weighted_distance = 0

    for _, n in neighborhoods.iterrows():

        distances = []

        for _, w in warehouses.iterrows():

            distance = calculate_distance(
                n["Latitude"],
                n["Longitude"],
                w["Latitude"],
                w["Longitude"]
            )

            distances.append(
                (distance, w["Warehouse"])
            )

        nearest_distance, nearest_warehouse = min(
            distances,
            key=lambda x: x[0]
        )

        weighted_distance = (
            nearest_distance * n["Daily Orders"]
        )

        total_weighted_distance += weighted_distance

        assignments.append([
            n["Neighborhood"],
            nearest_warehouse,
            nearest_distance,
            n["Daily Orders"],
            weighted_distance
        ])

    return pd.DataFrame(
        assignments,
        columns=[
            "Neighborhood",
            "Assigned Warehouse",
            "Distance (km)",
            "Daily Orders",
            "Weighted Distance"
        ]
    ), total_weighted_distance


# ---------------------------------------------------------
# OPTIMIZATION
# ---------------------------------------------------------

def optimize_warehouses(neighborhoods, number_of_warehouses):

    best_combination = None
    best_cost = float("inf")

    candidate_indices = list(range(len(neighborhoods)))

    for combination in combinations(
        candidate_indices,
        number_of_warehouses
    ):

        total_cost = 0

        for _, n in neighborhoods.iterrows():

            minimum_distance = float("inf")

            for index in combination:

                candidate = neighborhoods.iloc[index]

                distance = calculate_distance(
                    n["Latitude"],
                    n["Longitude"],
                    candidate["Latitude"],
                    candidate["Longitude"]
                )

                if distance < minimum_distance:
                    minimum_distance = distance

            total_cost += (
                minimum_distance * n["Daily Orders"]
            )

        if total_cost < best_cost:

            best_cost = total_cost
            best_combination = combination

    return best_combination, best_cost


# ---------------------------------------------------------
# OPTIMIZATION BUTTON
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">🚀 Optimization</div>',
    unsafe_allow_html=True
)

number_of_warehouses = len(warehouses)

if number_of_warehouses > len(neighborhoods):

    st.error(
        "Number of warehouses cannot exceed number of neighborhoods."
    )

else:

    if st.button(
        "🚀 Run Warehouse Optimization",
        type="primary",
        use_container_width=True
    ):

        with st.spinner("Finding optimal warehouse locations..."):

            # Current arrangement
            current_assignments, current_distance = (
                calculate_assignments(
                    neighborhoods,
                    warehouses
                )
            )

            # Optimize
            best_indices, optimized_distance = (
                optimize_warehouses(
                    neighborhoods,
                    number_of_warehouses
                )
            )

            optimized_warehouses = neighborhoods.iloc[
                list(best_indices)
            ].copy()

            optimized_warehouses["Warehouse"] = (
                optimized_warehouses["Neighborhood"]
                + " Warehouse"
            )

            optimized_assignments, _ = (
                calculate_assignments(
                    neighborhoods,
                    optimized_warehouses[
                        [
                            "Warehouse",
                            "Latitude",
                            "Longitude"
                        ]
                    ]
                )
            )

            reduction = (
                current_distance
                - optimized_distance
            )

            percentage_reduction = (
                reduction / current_distance * 100
                if current_distance != 0
                else 0
            )

        # Store results
        st.session_state["optimized"] = True
        st.session_state["current_distance"] = current_distance
        st.session_state["optimized_distance"] = optimized_distance
        st.session_state["reduction"] = reduction
        st.session_state["percentage_reduction"] = percentage_reduction
        st.session_state["optimized_warehouses"] = optimized_warehouses
        st.session_state["optimized_assignments"] = optimized_assignments


# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

if st.session_state.get("optimized", False):

    current_distance = st.session_state["current_distance"]
    optimized_distance = st.session_state["optimized_distance"]
    reduction = st.session_state["reduction"]
    percentage_reduction = st.session_state["percentage_reduction"]

    optimized_warehouses = st.session_state[
        "optimized_warehouses"
    ]

    optimized_assignments = st.session_state[
        "optimized_assignments"
    ]

    st.markdown(
        '<div class="section-title">📈 Optimization Results</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">
                    {current_distance:,.2f}
                </div>
                <div class="metric-label">
                    Current Distance (order-km)
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">
                    {optimized_distance:,.2f}
                </div>
                <div class="metric-label">
                    Optimized Distance (order-km)
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">
                    {reduction:,.2f}
                </div>
                <div class="metric-label">
                    Distance Reduction
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">
                    {percentage_reduction:.2f}%
                </div>
                <div class="metric-label">
                    Improvement
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # RECOMMENDED WAREHOUSES
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">🏭 Recommended Warehouse Locations</div>',
        unsafe_allow_html=True
    )

    warehouse_columns = st.columns(
        len(optimized_warehouses)
    )

    for i, (_, warehouse) in enumerate(
        optimized_warehouses.iterrows()
    ):

        with warehouse_columns[i]:

            st.markdown(
                f"""
                <div class="warehouse-card">
                    <h4>🟢 {warehouse["Warehouse"]}</h4>
                    <b>Location:</b> {warehouse["Neighborhood"]}<br>
                    <b>Latitude:</b> {warehouse["Latitude"]:.6f}<br>
                    <b>Longitude:</b> {warehouse["Longitude"]:.6f}
                </div>
                """,
                unsafe_allow_html=True
            )


    # -----------------------------------------------------
    # ASSIGNMENTS
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">📦 Neighborhood Assignments</div>',
        unsafe_allow_html=True
    )

    display_assignments = optimized_assignments.copy()

    display_assignments["Distance (km)"] = (
        display_assignments["Distance (km)"].round(2)
    )

    display_assignments["Weighted Distance"] = (
        display_assignments["Weighted Distance"].round(2)
    )

    st.dataframe(
        display_assignments,
        use_container_width=True,
        hide_index=True
    )


    # -----------------------------------------------------
    # MAP DATA
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">🗺️ Demand & Warehouse Map</div>',
        unsafe_allow_html=True
    )

    map_neighborhoods = neighborhoods.copy()

    def demand_category(orders):

        if orders >= 120:
            return "High"

        elif orders >= 80:
            return "Moderate"

        else:
            return "Low"


    def demand_color(orders):

        if orders >= 120:
            return [220, 38, 38]

        elif orders >= 80:
            return [234, 179, 8]

        else:
            return [107, 114, 128]


    map_neighborhoods["Demand"] = (
        map_neighborhoods["Daily Orders"]
        .apply(demand_category)
    )

    map_neighborhoods["Color"] = (
        map_neighborhoods["Daily Orders"]
        .apply(demand_color)
    )

    map_neighborhoods["Radius"] = (
        400 + map_neighborhoods["Daily Orders"] * 4
    )


    map_warehouses = optimized_warehouses[
        [
            "Warehouse",
            "Latitude",
            "Longitude"
        ]
    ].copy()

    map_warehouses["Color"] = [
        [34, 197, 94]
        for _ in range(len(map_warehouses))
    ]

    map_warehouses["Radius"] = 900


    # -----------------------------------------------------
    # PYDECK LAYERS
    # -----------------------------------------------------

    neighborhood_layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_neighborhoods,
        get_position="[Longitude, Latitude]",
        get_fill_color="Color",
        get_radius="Radius",
        pickable=True,
        opacity=0.85,
        stroked=True,
        get_line_color=[255, 255, 255],
        line_width_min_pixels=1
    )


    warehouse_layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_warehouses,
        get_position="[Longitude, Latitude]",
        get_fill_color="Color",
        get_radius="Radius",
        pickable=True,
        opacity=1,
        stroked=True,
        get_line_color=[255, 255, 255],
        line_width_min_pixels=2
    )


    # -----------------------------------------------------
    # MAP VIEW
    # -----------------------------------------------------

    view_state = pdk.ViewState(
        latitude=12.9716,
        longitude=77.5946,
        zoom=10.5,
        pitch=0
    )


    # -----------------------------------------------------
    # TOOLTIP
    # -----------------------------------------------------

    tooltip = {
        "html": """
        <b>{Neighborhood}</b><br/>
        Daily Orders: {Daily Orders}<br/>
        Demand: {Demand}
        """,
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }


    # -----------------------------------------------------
    # MAP
    # -----------------------------------------------------

    deck = pdk.Deck(
        layers=[
            neighborhood_layer,
            warehouse_layer
        ],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style=None
    )

    st.pydeck_chart(
        deck,
        use_container_width=True
    )


    # -----------------------------------------------------
    # MAP LEGEND
    # -----------------------------------------------------

    st.markdown(
        """
        **Map Legend**

        🔴 **High Demand** — 120+ orders/day &nbsp;&nbsp;&nbsp;
        🟡 **Moderate Demand** — 80–119 orders/day &nbsp;&nbsp;&nbsp;
        ⚪ **Low Demand** — below 80 orders/day &nbsp;&nbsp;&nbsp;
        🟢 **Optimized Warehouse**
        """
    )


    # -----------------------------------------------------
    # METHODOLOGY
    # -----------------------------------------------------

    with st.expander("🧠 How GridPoint Optimizes Warehouses"):

        st.markdown("""
        GridPoint uses a **K-Median-style optimization approach**.

        **1. Candidate locations**

        Existing neighborhoods are treated as candidate warehouse
        locations.

        **2. Distance calculation**

        The Haversine formula calculates the geographic distance
        between neighborhoods and warehouses.

        **3. Demand weighting**

        Delivery distance is multiplied by the neighborhood's
        daily order volume.

        **4. Optimization**

        GridPoint evaluates possible combinations of warehouse
        locations and selects the combination that minimizes:

        **Total Cost = Σ (Distance × Daily Orders)**

        **5. Assignment**

        Each neighborhood is assigned to its nearest optimized
        warehouse.

        This ensures that high-demand neighborhoods have a larger
        influence on the warehouse placement decision.
        """)


else:

    st.info(
        "Enter or review your data, then click "
        "**Run Warehouse Optimization** to generate results."
    )

