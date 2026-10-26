
import streamlit as st
import pandas as pd

from datetime import date, time
from database import create_booking, get_all_bookings

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="EV ChargeHub",
    page_icon="⚡",
    layout="wide"
)

# ==========================================
# CUSTOM DESIGN
# ==========================================
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #f4f7fb;
    color: #1f2937;
}

/* Headings */
.stApp h1,
.stApp h2,
.stApp h3 {
    color: #12345a !important;
}

/* Main content text */
.stApp p,
.stApp li,
.stApp label,
.stApp [data-testid="stMarkdownContainer"] {
    color: #253247;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #202632;
}

section[data-testid="stSidebar"] * {
    color: #ffffff;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background-color: #087f5b;
    color: white !important;
    border-radius: 8px;
    border: none;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #066b4c;
    color: white !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #e1e8f0;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {
    color: #12345a !important;
}

/* Data tables */
[data-testid="stDataFrame"] {
    background-color: white;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SAMPLE STATIONS
# ==========================================
stations = [
    {
        "name": "Chennai Central Charging Hub",
        "location": "Chennai",
        "power": 60,
        "price": 8,
        "status": "Available"
    },
    {
        "name": "Tambaram EV Point",
        "location": "Tambaram",
        "power": 30,
        "price": 7,
        "status": "Available"
    },
    {
        "name": "Guindy Fast Charge",
        "location": "Guindy",
        "power": 120,
        "price": 10,
        "status": "Available"
    }
]

station_names = [s["name"] for s in stations]

# ==========================================
# HEADER
# ==========================================
st.title("⚡ EV ChargeHub")

st.subheader(
    "Smart EV Charging. Simple Booking. Transparent Billing."
)

st.write(
    "Find charging stations, book charging slots, "
    "estimate charging costs, and manage bookings."
)

st.info(
    "Project demonstration: station listings and availability "
    "are sample data. Booking records are stored in Supabase."
)

# ==========================================
# NAVIGATION
# ==========================================
page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Charging Stations",
        "Book a Slot",
        "Cost Calculator",
        "My Bookings",
        "Admin Dashboard"
    ]
)

# ==========================================
# DATABASE HELPER
# ==========================================
def load_bookings():
    """Retrieve bookings from the configured database."""
    result = get_all_bookings()

    if result is None:
        raise ValueError(
            "get_all_bookings() returned None. "
            "Check database.py."
        )

    if not isinstance(result, list):
        raise TypeError(
            "Expected a list from get_all_bookings()."
        )

    return result


# ==========================================
# HOME
# ==========================================
if page == "Home":

    st.header("Welcome to the Future of EV Charging")

    try:
        bookings = load_bookings()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Charging Stations",
            len(stations)
        )

        col2.metric(
            "Total Bookings",
            len(bookings)
        )

        col3.metric(
            "Platform",
            "Online"
        )

    except Exception as e:
        st.error("Database connection failed.")
        st.code(repr(e))

    st.divider()

    st.header("Why EV ChargeHub?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🔌 Find Stations")
        st.write(
            "Explore charging station locations, "
            "charging power, and prices."
        )

    with col2:
        st.subheader("📅 Book a Slot")
        st.write(
            "Create a booking and receive a booking ID."
        )

    with col3:
        st.subheader("🧾 Transparent Billing")
        st.write(
            "Estimate charging costs and download invoices."
        )

# ==========================================
# CHARGING STATIONS
# ==========================================
elif page == "Charging Stations":

    st.header("🔌 Charging Stations")

    for station in stations:

        with st.container(border=True):

            st.subheader(station["name"])

            col1, col2 = st.columns(2)

            col1.write(
                f"📍 Location: {station['location']}"
            )

            col1.write(
                f"⚡ Power: {station['power']} kW"
            )

            col2.write(
                f"💰 Price: ₹{station['price']} / kWh"
            )

            col2.success(station["status"])

    st.caption(
        "Sample station data only. Live charger availability "
        "has not been verified."
    )

# ==========================================
# BOOK A SLOT
# ==========================================
elif page == "Book a Slot":

    st.header("📅 Book a Charging Slot")

    with st.form("booking_form"):

        customer = st.text_input(
            "Customer name"
        )

        vehicle = st.text_input(
            "Vehicle model"
        )

        selected_station = st.selectbox(
            "Select charging station",
            station_names
        )

        booking_date = st.date_input(
            "Booking date",
            min_value=date.today()
        )

        booking_time = st.time_input(
            "Booking time",
            value=time(10, 0)
        )

        energy = st.number_input(
            "Energy required (kWh)",
            min_value=1.0,
            max_value=200.0,
            value=20.0,
            step=1.0
        )

        submitted = st.form_submit_button(
            "Confirm Booking"
        )

    if submitted:

        if not customer.strip() or not vehicle.strip():

            st.error(
                "Enter your name and vehicle model."
            )

        else:

            station = next(
                item for item in stations
                if item["name"] == selected_station
            )

            estimated_bill = energy * station["price"]

            try:
                booking_id, bill = create_booking(
                    customer.strip(),
                    vehicle.strip(),
                    selected_station,
                    booking_date,
                    booking_time,
                    energy,
                    station["price"]
                )

                st.success(
                    "Booking created successfully!"
                )

                st.write("Your Booking ID:")

                st.code(str(booking_id))

                st.metric(
                    "Estimated Bill",
                    f"₹{float(bill):.2f}"
                )

                st.info(
                    "Keep your booking ID for future reference."
                )

            except Exception as e:

                st.error(
                    "Booking could not be saved."
                )

                st.code(repr(e))

# ==========================================
# COST CALCULATOR
# ==========================================
elif page == "Cost Calculator":

    st.header("🔋 Charging Cost Calculator")

    capacity = st.number_input(
        "Battery capacity (kWh)",
        min_value=1.0,
        max_value=250.0,
        value=60.0
    )

    initial = st.slider(
        "Initial battery level (%)",
        min_value=0,
        max_value=99,
        value=20
    )

    target = st.slider(
        "Target battery level (%)",
        min_value=1,
        max_value=100,
        value=80
    )

    rate = st.number_input(
        "Charging price (₹/kWh)",
        min_value=0.1,
        value=8.0
    )

    if target <= initial:

        st.warning(
            "Target battery level must exceed "
            "the initial battery level."
        )

    else:

        energy_needed = (
            capacity * (target - initial) / 100
        )

        estimated_cost = energy_needed * rate

        col1, col2 = st.columns(2)

        col1.metric(
            "Energy Required",
            f"{energy_needed:.2f} kWh"
        )

        col2.metric(
            "Estimated Charging Cost",
            f"₹{estimated_cost:.2f}"
        )

        st.caption(
            "Estimate assumes ideal charging. Actual costs "
            "may be higher due to charging losses, "
            "tariffs, and extra fees."
        )

# ==========================================
# MY BOOKINGS
# ==========================================
elif page == "My Bookings":

    st.header("📋 Booking History")

    try:
        bookings = load_bookings()

        if bookings:

            df = pd.DataFrame(bookings)

            st.subheader("All Booking Records")

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            # Check required columns
            if "Booking ID" not in df.columns:

                st.warning(
                    "Booking ID column is missing. "
                    "Check the column names in database.py."
                )

            else:

                booking_ids = df["Booking ID"].tolist()

                selected_id = st.selectbox(
                    "Select booking for invoice",
                    booking_ids
                )

                booking = next(
                    item for item in bookings
                    if str(item["Booking ID"])
                    == str(selected_id)
                )

                invoice = f"""
EV CHARGEHUB
SIMULATED INVOICE

Booking ID: {booking.get('Booking ID', '')}
Customer: {booking.get('Customer', '')}
Vehicle: {booking.get('Vehicle', '')}
Station: {booking.get('Station', '')}
Date: {booking.get('Date', '')}
Time: {booking.get('Time', '')}

Energy: {booking.get('Energy (kWh)', '')} kWh
Price per kWh: ₹{booking.get('Price (₹)', '')}
Estimated total: ₹{booking.get('Estimated Bill (₹)', '')}

Status: {booking.get('Status', '')}

This is a simulated invoice.
This is not a payment receipt.
"""

                st.subheader("Invoice")

                st.text(invoice)

                st.download_button(
                    label="Download Invoice",
                    data=invoice,
                    file_name=f"{selected_id}_invoice.txt",
                    mime="text/plain"
                )

        else:

            st.info(
                "No bookings found. Create your first booking."
            )

    except Exception as e:

        st.error(
            "Unable to retrieve bookings."
        )

        st.write(
            "Database error details:"
        )

        st.code(repr(e))

        st.info(
            "Check your Supabase settings, table name, "
            "permissions, and database.py."
        )

# ==========================================
# ADMIN DASHBOARD
# ==========================================
elif page == "Admin Dashboard":

    st.header("📊 Admin Dashboard")

    try:
        bookings = load_bookings()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Stations",
            len(stations)
        )

        col2.metric(
            "Total Bookings",
            len(bookings)
        )

        # Safely calculate booking value
        total_value = 0.0

        for item in bookings:
            value = item.get(
                "Estimated Bill (₹)", 0
            )

            total_value += float(value or 0)

        col3.metric(
            "Estimated Booking Value",
            f"₹{total_value:.2f}"
        )

        st.divider()

        st.subheader(
            "🔌 Charging Station Details"
        )

        st.dataframe(
            pd.DataFrame(stations),
            use_container_width=True,
            hide_index=True
        )

        st.subheader(
            "📋 Recent Bookings"
        )

        if bookings:

            booking_df = pd.DataFrame(bookings)

            # Show newest records first if Date exists
            if "Date" in booking_df.columns:
                booking_df = booking_df.sort_values(
                    by="Date",
                    ascending=False
                )

            st.dataframe(
                booking_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No bookings have been created yet."
            )

    except Exception as e:

        st.error(
            "Unable to load dashboard data."
        )

        st.code(repr(e))

# ==========================================
# FOOTER
# ==========================================
st.divider()

st.caption(
    "EV ChargeHub | Smart EV Charging "
    "Station Management System"
)
