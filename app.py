import streamlit as st
import pandas as pd
import pydeck as pdk
from math import radians, sin, cos, sqrt, atan2
from itertools import combinations


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="OptiGrid",
    page_icon="📍",
    layout="wide"
)


# =========================================================
# CUSTOM THEME
# =========================================================

theme = st.sidebar.radio(
    "🎨 Appearance",
    ["Light Mode", "Dark Mode"]
)


if theme == "Dark Mode":
    st.markdown(
        """
        <style>
        /* ---------- GLOBAL ---------- */

        .stApp {
            background: #0b1120;
            color: #e5e7eb;
        }

        [data-testid="stAppViewContainer"] {
            background: #0b1120;
        }

        [data-testid="stHeader"] {
            background: #0b1120;
        }

        [data-testid="stSidebar"] {
            background: #111827;
            border-right: 1px solid #1f2937;
        }

        [data-testid="stSidebar"] * {
            color: #e5e7eb !important;
        }

        /* ---------- MAIN TEXT ---------- */

        h1, h2, h3, h4, h5, h6 {
            color: #f8fafc !important;
        }

        p, li, label, span {
            color: #d1d5db;
        }

        /* ---------- HEADER ---------- */

        .main-title {
            font-size: 3rem;
            font-weight: 800;
            color: #f8fafc !important;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            font-size: 1.1rem;
            color: #94a3b8 !important;
            margin-bottom: 1.5rem;
        }

        /* ---------- SECTION ---------- */

        .section-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: #f8fafc !important;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
        }

        /* ---------- CARDS ---------- */

        .metric-card {
            background: #111827;
            border: 1px solid #243044;
            border-radius: 14px;
            padding: 1.1rem;
            min-height: 125px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
        }

        .metric-label {
            color: #94a3b8 !important;
            font-size: 0.9rem;
            margin-bottom: 0.35rem;
        }

        .metric-value {
            color: #f8fafc !important;
            font-size: 1.55rem;
            font-weight: 750;
        }

        .metric-highlight {
            color: #4ade80 !important;
        }

        /* ---------- INFO BOX ---------- */

        .info-box {
            background: #111827;
            border: 1px solid #263449;
            border-radius: 12px;
            padding: 1rem 1.2rem;
            margin: 1rem 0;
        }

        .info-box strong {
            color: #f8fafc !important;
        }

        /* ---------- WAREHOUSE CARDS ---------- */

        .warehouse-card {
            background: #0f172a;
            border: 1px solid #14532d;
            border-left: 5px solid #22c55e;
            border-radius: 12px;
            padding: 1rem 1.2rem;
            margin-bottom: 0.7rem;
        }

        .warehouse-title {
            color: #86efac !important;
            font-weight: 700;
            font-size: 1.05rem;
        }

        .warehouse-text {
            color: #cbd5e1 !important;
            margin-top: 0.25rem;
        }

        /* ---------- INPUTS ---------- */

        div[data-baseweb="input"] {
            background-color: #111827 !important;
            border-color: #334155 !important;
        }

        div[data-baseweb="input"] input {
            color: #f8fafc !important;
            background-color: #111827 !important;
        }

        div[data-baseweb="select"] > div {
            background-color: #111827 !important;
            border-color: #334155 !important;
            color: #f8fafc !important;
        }

        textarea {
            background-color: #111827 !important;
            color: #f8fafc !important;
        }

        /* ---------- BUTTONS ---------- */

        .stButton > button {
            background: #2563eb;
            color: white !important;
            border: none;
            border-radius: 9px;
            font-weight: 650;
            padding: 0.55rem 1.1rem;
        }

        .stButton > button:hover {
            background: #1d4ed8;
            color: white !important;
        }

        /* ---------- TABLES ---------- */

        [data-testid="stDataFrame"] {
            border: 1px solid #263449;
            border-radius: 10px;
        }

        /* ---------- EXPANDERS ---------- */

        [data-testid="stExpander"] {
            background: #111827;
            border: 1px solid #263449;
            border-radius: 10px;
        }

        /* ---------- DIVIDERS ---------- */

        hr {
            border-color: #263449 !important;
        }

        /* ---------- ALERTS ---------- */

        [data-testid="stAlert"] {
            background: #111827;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

else:
    st.markdown(
        """
        <style>
        /* ---------- GLOBAL ---------- */

        .stApp {
            background: #f8fafc;
            color: #1e293b;
        }

        [data-testid="stAppViewContainer"] {
            background: #f8fafc;
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e2e8f0;
        }

        /* ---------- HEADER ---------- */

        .main-title {
            font-size: 3rem;
            font-weight: 800;
            color: #0f172a !important;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            font-size: 1.1rem;
            color: #64748b !important;
            margin-bottom: 1.5rem;
        }

        /* ---------- SECTION ---------- */

        .section-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: #0f172a !important;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
        }

        /* ---------- CARDS ---------- */

        .metric-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 1.1rem;
            min-height: 125px;
            box-shadow: 0 3px 12px rgba(15, 23, 42, 0.06);
        }

        .metric-label {
            color: #64748b !important;
            font-size: 0.9rem;
            margin-bottom: 0.35rem;
        }

        .metric-value {
            color: #0f172a !important;
            font-size: 1.55rem;
            font-weight: 750;
        }

        .metric-highlight {
            color: #15803d !important;
        }

        /* ---------- INFO BOX ---------- */

        .info-box {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1rem 1.2rem;
            margin: 1rem 0;
        }

        /* ---------- WAREHOUSE CARDS ---------- */

        .warehouse-card {
            background: #f0fdf4;
            border: 1px solid #bbf7d0;
            border-left: 5px solid #16a34a;
            border-radius: 12px;
            padding: 1rem 1.2rem;
            margin-bottom: 0.7rem;
        }

        .warehouse-title {
            color: #166534 !important;
            font-weight: 700;
            font-size: 1.05rem;
        }

        .warehouse-text {
            color: #475569 !important;
            margin-top: 0.25rem;
        }

        /* ---------- BUTTONS ---------- */

        .stButton > button {
            background: #2563eb;
            color: white !important;
            border: none;
            border-radius: 9px;
            font-weight: 650;
            padding: 0.55rem 1.1rem;
        }

        .stButton > button:hover {
            background: #1d4ed8;
            color: white !important;
        }

        /* ---------- EXPANDERS ---------- */

        [data-testid="stExpander"] {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="main-title">📍 OptiGrid</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Warehouse Location Optimization Platform</div>',
    unsafe_allow_html=True
)


# =========================================================
# DEMO DATA
# =========================================================

demo_neighborhoods = pd.DataFrame([
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
], columns=[
    "Neighborhood",
    "Latitude",
    "Longitude",
    "Daily Orders"
])


demo_warehouses = pd.DataFrame([
    ["Yeshwanthpur Warehouse", 13.0285, 77.5548],
    ["Whitefield Warehouse", 12.9698, 77.7500],
    ["Electronic City Warehouse", 12.8452, 77.6602]
], columns=[
    "Warehouse",
    "Latitude",
    "Longitude"
])


# =========================================================
# HAVERSINE DISTANCE
# =========================================================

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


# =========================================================
# FAST K-MEDIAN STYLE OPTIMIZATION
# =========================================================

def optimize_warehouses(neighborhoods, number_of_warehouses):

    n = len(neighborhoods)

    # Precompute distance matrix
    distance_matrix = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):

            distance = calculate_distance(
                neighborhoods.iloc[i]["Latitude"],
                neighborhoods.iloc[i]["Longitude"],
                neighborhoods.iloc[j]["Latitude"],
                neighborhoods.iloc[j]["Longitude"]
            )

            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance

    demand = neighborhoods["Daily Orders"].tolist()

    best_combination = None
    best_cost = float("inf")

    for combination in combinations(
        range(n),
        number_of_warehouses
    ):

        total_cost = 0.0

        for neighborhood_index in range(n):

            minimum_distance = min(
                distance_matrix[neighborhood_index][warehouse_index]
                for warehouse_index in combination
            )

            total_cost += (
                minimum_distance
                * demand[neighborhood_index]
            )

        if total_cost < best_cost:
            best_cost = total_cost
            best_combination = combination

    return best_combination, best_cost


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## ⚙️ OptiGrid Controls")

mode = st.sidebar.radio(
    "Data Mode",
    ["Demo Mode", "Manual Mode"]
)


# =========================================================
# DATA SELECTION
# =========================================================

if mode == "Demo Mode":

    neighborhoods = demo_neighborhoods.copy()
    warehouses = demo_warehouses.copy()

    st.sidebar.success(
        "Demo dataset loaded: 25 Bengaluru neighborhoods"
    )

else:

    st.sidebar.info(
        "Enter neighborhood and warehouse data below."
    )

    number_of_neighborhoods = st.sidebar.number_input(
        "Number of Neighborhoods",
        min_value=2,
        max_value=50,
        value=5,
        step=1
    )

    neighborhood_rows = []

    for i in range(number_of_neighborhoods):

        with st.expander(
            f"Neighborhood {i + 1}"
        ):

            name = st.text_input(
                "Neighborhood Name",
                value=f"Neighborhood {i + 1}",
                key=f"name_{i}"
            )

            latitude = st.number_input(
                "Latitude",
                value=12.9716,
                format="%.6f",
                key=f"lat_{i}"
            )

            longitude = st.number_input(
                "Longitude",
                value=77.5946,
                format="%.6f",
                key=f"lon_{i}"
            )

            orders = st.number_input(
                "Daily Orders",
                min_value=1,
                value=100,
                step=1,
                key=f"orders_{i}"
            )

            neighborhood_rows.append([
                name,
                latitude,
                longitude,
                orders
            ])

    neighborhoods = pd.DataFrame(
        neighborhood_rows,
        columns=[
            "Neighborhood",
            "Latitude",
            "Longitude",
            "Daily Orders"
        ]
    )

    number_of_initial_warehouses = st.sidebar.number_input(
        "Number of Existing Warehouses",
        min_value=1,
        max_value=10,
        value=2,
        step=1
    )

    warehouse_rows = []

    for i in range(number_of_initial_warehouses):

        with st.expander(
            f"Existing Warehouse {i + 1}"
        ):

            name = st.text_input(
                "Warehouse Name",
                value=f"Warehouse {i + 1}",
                key=f"warehouse_name_{i}"
            )

            latitude = st.number_input(
                "Latitude",
                value=12.9716,
                format="%.6f",
                key=f"warehouse_lat_{i}"
            )

            longitude = st.number_input(
                "Longitude",
                value=77.5946,
                format="%.6f",
                key=f"warehouse_lon_{i}"
            )

            warehouse_rows.append([
                name,
                latitude,
                longitude
            ])

    warehouses = pd.DataFrame(
        warehouse_rows,
        columns=[
            "Warehouse",
            "Latitude",
            "Longitude"
        ]
    )


# =========================================================
# SUMMARY
# =========================================================

st.markdown(
    '<div class="section-title">📊 Network Overview</div>',
    unsafe_allow_html=True
)

total_orders = int(
    neighborhoods["Daily Orders"].sum()
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Neighborhoods</div>
            <div class="metric-value">
                {len(neighborhoods)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Existing Warehouses</div>
            <div class="metric-value">
                {len(warehouses)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Total Daily Orders</div>
            <div class="metric-value">
                {total_orders:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# NEIGHBORHOOD DATA
# =========================================================

st.markdown(
    '<div class="section-title">🏘️ Neighborhood Demand</div>',
    unsafe_allow_html=True
)

display_neighborhoods = neighborhoods.copy()

display_neighborhoods["Demand Level"] = display_neighborhoods[
    "Daily Orders"
].apply(
    lambda x:
        "High" if x >= 120
        else "Moderate" if x >= 80
        else "Low"
)

st.dataframe(
    display_neighborhoods,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# WAREHOUSE DATA
# =========================================================

st.markdown(
    '<div class="section-title">🏭 Existing Warehouses</div>',
    unsafe_allow_html=True
)

st.dataframe(
    warehouses,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# CURRENT ASSIGNMENTS
# =========================================================

current_assignments = []

current_total_distance = 0.0

for _, neighborhood in neighborhoods.iterrows():

    distances = []

    for _, warehouse in warehouses.iterrows():

        distance = calculate_distance(
            neighborhood["Latitude"],
            neighborhood["Longitude"],
            warehouse["Latitude"],
            warehouse["Longitude"]
        )

        distances.append(
            (distance, warehouse["Warehouse"])
        )

    nearest_distance, nearest_warehouse = min(
        distances,
        key=lambda x: x[0]
    )

    weighted_distance = (
        nearest_distance
        * neighborhood["Daily Orders"]
    )

    current_total_distance += weighted_distance

    current_assignments.append([
        neighborhood["Neighborhood"],
        nearest_warehouse,
        nearest_distance,
        neighborhood["Daily Orders"],
        weighted_distance
    ])


current_df = pd.DataFrame(
    current_assignments,
    columns=[
        "Neighborhood",
        "Assigned Warehouse",
        "Distance (km)",
        "Daily Orders",
        "Weighted Distance"
    ]
)


# =========================================================
# OPTIMIZATION CONTROL
# =========================================================

st.markdown(
    '<div class="section-title">🚀 Warehouse Optimization</div>',
    unsafe_allow_html=True
)

max_warehouses = len(neighborhoods)

default_warehouses = min(
    3,
    max_warehouses
)

number_of_warehouses = st.slider(
    "Select number of optimized warehouses",
    min_value=1,
    max_value=max_warehouses,
    value=default_warehouses
)

st.markdown(
    """
    <div class="info-box">
        <strong>Optimization objective:</strong>
        Find warehouse locations that minimize total
        order-weighted delivery distance.
    </div>
    """,
    unsafe_allow_html=True
)


if st.button(
    "🔍 Optimize Warehouse Locations",
    use_container_width=True
):

    if number_of_warehouses > len(neighborhoods):

        st.error(
            "Number of warehouses cannot exceed "
            "the number of neighborhoods."
        )

    else:

        with st.spinner(
            "Calculating optimal warehouse locations..."
        ):

            best_combination, optimized_distance = (
                optimize_warehouses(
                    neighborhoods,
                    number_of_warehouses
                )
            )

        st.session_state["best_combination"] = (
            best_combination
        )

        st.session_state["optimized_distance"] = (
            optimized_distance
        )

        st.session_state["optimized_ready"] = True


# =========================================================
# RESULTS
# =========================================================

if st.session_state.get(
    "optimized_ready",
    False
):

    best_combination = st.session_state[
        "best_combination"
    ]

    optimized_distance = st.session_state[
        "optimized_distance"
    ]

    distance_reduction = (
        current_total_distance
        - optimized_distance
    )

    if current_total_distance > 0:

        percentage_reduction = (
            distance_reduction
            / current_total_distance
        ) * 100

    else:
        percentage_reduction = 0

    st.markdown(
        '<div class="section-title">📈 Optimization Results</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    Current Distance
                </div>
                <div class="metric-value">
                    {current_total_distance:,.2f}
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
                    {optimized_distance:,.2f}
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
                <div class="metric-value metric-highlight">
                    {distance_reduction:,.2f}
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
                <div class="metric-value metric-highlight">
                    {percentage_reduction:.2f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # RECOMMENDED WAREHOUSES
    # =====================================================

    st.markdown(
        '<div class="section-title">📍 Recommended Warehouse Locations</div>',
        unsafe_allow_html=True
    )

    optimized_warehouses = []

    for index in best_combination:

        warehouse = neighborhoods.iloc[index]

        optimized_warehouses.append([
            warehouse["Neighborhood"],
            warehouse["Latitude"],
            warehouse["Longitude"]
        ])

        st.markdown(
            f"""
            <div class="warehouse-card">
                <div class="warehouse-title">
                    🟢 {warehouse["Neighborhood"]}
                </div>
                <div class="warehouse-text">
                    Latitude: {warehouse["Latitude"]:.6f}
                    &nbsp;&nbsp;|&nbsp;&nbsp;
                    Longitude: {warehouse["Longitude"]:.6f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # OPTIMIZED ASSIGNMENTS
    # =====================================================

    optimized_assignments = []

    for _, neighborhood in neighborhoods.iterrows():

        best_warehouse = None
        best_distance = float("inf")

        for index in best_combination:

            warehouse = neighborhoods.iloc[index]

            distance = calculate_distance(
                neighborhood["Latitude"],
                neighborhood["Longitude"],
                warehouse["Latitude"],
                warehouse["Longitude"]
            )

            if distance < best_distance:

                best_distance = distance
                best_warehouse = warehouse["Neighborhood"]

        optimized_assignments.append([
            neighborhood["Neighborhood"],
            best_warehouse,
            best_distance,
            neighborhood["Daily Orders"],
            best_distance * neighborhood["Daily Orders"]
        ])


    optimized_df = pd.DataFrame(
        optimized_assignments,
        columns=[
            "Neighborhood",
            "Optimized Warehouse",
            "Distance (km)",
            "Daily Orders",
            "Weighted Distance"
        ]
    )

    st.markdown(
        '<div class="section-title">🔗 Optimized Assignments</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        optimized_df,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # MAP
    # =====================================================

    st.markdown(
        '<div class="section-title">🗺️ Optimized Network Map</div>',
        unsafe_allow_html=True
    )

    map_data = []

    for _, row in neighborhoods.iterrows():

        orders = row["Daily Orders"]

        if orders >= 120:

            color = [220, 38, 38]
            demand_level = "High"

        elif orders >= 80:

            color = [234, 179, 8]
            demand_level = "Moderate"

        else:

            color = [107, 114, 128]
            demand_level = "Low"

        map_data.append({
            "Name": row["Neighborhood"],
            "Latitude": row["Latitude"],
            "Longitude": row["Longitude"],
            "Daily Orders": int(orders),
            "Demand Level": demand_level,
            "Color": color,
            "Radius": 400 + (orders * 4)
        })


    warehouse_map_data = []

    for index in best_combination:

        row = neighborhoods.iloc[index]

        warehouse_map_data.append({
            "Warehouse": f"Optimized Warehouse — {row['Neighborhood']}",
            "Latitude": row["Latitude"],
            "Longitude": row["Longitude"],
            "Color": [34, 197, 94],
            "Radius": 1000
        })


    neighborhood_layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_data,
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
        data=warehouse_map_data,
        get_position="[Longitude, Latitude]",
        get_fill_color="Color",
        get_radius="Radius",
        pickable=True,
        opacity=1,
        stroked=True,
        get_line_color=[255, 255, 255],
        line_width_min_pixels=3
    )


    view_state = pdk.ViewState(
        latitude=12.9716,
        longitude=77.5946,
        zoom=10.5,
        pitch=0
    )


    tooltip = {
        "html": """
        <b>{Name}</b><br/>
        Daily Orders: {Daily Orders}<br/>
        Demand: {Demand Level}
        """,
        "style": {
            "backgroundColor": "#111827",
            "color": "white"
        }
    }


    warehouse_tooltip = {
        "html": """
        <b>{Warehouse}</b>
        """,
        "style": {
            "backgroundColor": "#14532d",
            "color": "white"
        }
    }


    neighborhood_deck = pdk.Deck(
        layers=[neighborhood_layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style=None
    )


    warehouse_deck = pdk.Deck(
        layers=[warehouse_layer],
        initial_view_state=view_state,
        tooltip=warehouse_tooltip,
        map_style=None
    )


    st.pydeck_chart(
        pdk.Deck(
            layers=[
                neighborhood_layer,
                warehouse_layer
            ],
            initial_view_state=view_state,
            tooltip=tooltip,
            map_style=None
        ),
        use_container_width=True
    )


    # =====================================================
    # MAP LEGEND
    # =====================================================

    st.markdown(
        """
        <div class="info-box">

        <strong>Map Legend</strong><br><br>

        🔴 <b>High Demand</b> — 120+ daily orders
        &nbsp;&nbsp;&nbsp;

        🟡 <b>Moderate Demand</b> — 80–119 daily orders
        &nbsp;&nbsp;&nbsp;

        ⚪ <b>Low Demand</b> — below 80 daily orders
        &nbsp;&nbsp;&nbsp;

        🟢 <b>Optimized Warehouse</b>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# ALGORITHM EXPLANATION
# =========================================================

st.markdown(
    '<div class="section-title">🧠 How OptiGrid Works</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-box">

    <b>1. Geographic Distance</b><br>
    OptiGrid calculates distances between neighborhoods
    using the Haversine formula.

    <br><br>

    <b>2. Demand Weighting</b><br>
    Each distance is multiplied by the neighborhood's
    daily order volume, giving higher-demand areas
    greater importance.

    <br><br>

    <b>3. Warehouse Selection</b><br>
    Neighborhoods are treated as candidate warehouse
    locations. OptiGrid evaluates possible combinations
    of warehouse locations.

    <br><br>

    <b>4. Assignment</b><br>
    Every neighborhood is assigned to its nearest
    selected warehouse.

    <br><br>

    <b>5. Optimization Objective</b><br>
    The combination with the lowest total
    order-weighted delivery distance is selected.

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#64748b;">
        <b>OptiGrid</b> · Warehouse Location Optimization Platform
    </div>
    """,
    unsafe_allow_html=True
)