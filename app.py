import streamlit as st
import pandas as pd

from datetime import date, time
from database import create_booking, get_all_bookings

st.set_page_config(
page_title="EV ChargeHub",
page_icon="⚡",
layout="wide"
)


st.markdown("""

<style>
.stApp {
    background-color: #f4f7fb;
}

h1, h2, h3 {
    color: #12345a;
}

div.stButton > button {
    background-color: #087f5b;
    color: white;
    border-radius: 8px;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
}
</style>""", unsafe_allow_html=True)


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



st.title("⚡ EV ChargeHub")

st.subheader(
"Smart EV Charging. Simple Booking. Transparent Billing."
)

st.write(
"Find charging stations, book a charging slot, "
"estimate charging costs, and manage bookings."
)

st.info(
"Project demonstration: station listings and availability "
"are sample data. Booking records are stored in Supabase."
)



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



if page == "Home":

st.header("Welcome to the Future of EV Charging")

try:
    bookings = get_all_bookings()

    col1, col2, col3 = st.columns(3)

    col1.metric("Charging Stations", len(stations))
    col2.metric("Total Bookings", len(bookings))
    col3.metric("Platform", "Online")

except Exception:
    st.error(
        "Database connection failed. "
        "Check your Streamlit Secrets settings."
    )

st.divider()

st.header("Why EV ChargeHub?")

col1, col2, col3 = st.columns(3)

col1.write("🔌 **Find Charging Stations**")
col1.caption(
    "Explore station locations, charging power, and prices."
)

col2.write("📅 **Book a Charging Slot**")
col2.caption(
    "Create a booking and receive a unique booking ID."
)

col3.write("🧾 **Transparent Billing**")
col3.caption(
    "Estimate charging costs and download invoices."
)


elif page == "Charging Stations":

st.header("🔌 Charging Stations")

for station in stations:

    with st.container(border=True):

        st.subheader(station["name"])

        st.write("📍 Location:", station["location"])

        st.write(
            "⚡ Charging power:",
            f'{station["power"]} kW'
        )

        st.write(
            "💰 Price:",
            f'₹{station["price"]} per kWh'
        )

        st.success(station["status"])

st.caption(
    "Station information is illustrative and has not "
    "been verified as live station availability."
)


elif page == "Book a Slot":

st.header("📅 Book a Charging Slot")

station_names = [s["name"] for s in stations]

with st.form("booking_form"):

    customer = st.text_input("Customer name")

    vehicle = st.text_input("Vehicle model")

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

            st.success("Booking created successfully!")

            st.code(booking_id)

            st.metric(
                "Estimated Bill",
                f"₹{bill:.2f}"
            )

            st.info(
                "Keep your booking ID for future reference."
            )

        except Exception:
            st.error(
                "Booking could not be saved. "
                "Check the database configuration and try again."
            )


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
    0, 99, 20
)

target = st.slider(
    "Target battery level (%)",
    1, 100, 80
)

rate = st.number_input(
    "Charging price (₹/kWh)",
    min_value=0.1,
    value=8.0
)

if target <= initial:

    st.warning(
        "Target battery level must exceed the initial level."
    )

else:

    energy_needed = capacity * (
        (target - initial) / 100
    )

    estimated_cost = energy_needed * rate

    st.metric(
        "Energy Required",
        f"{energy_needed:.2f} kWh"
    )

    st.metric(
        "Estimated Charging Cost",
        f"₹{estimated_cost:.2f}"
    )

    st.caption(
        "This is an estimate. Actual costs may vary due "
        "to charging losses and station tariffs."
    )



elif page == "My Bookings":

st.header("📋 Booking History")

try:
    bookings = get_all_bookings()

    if bookings:

        df = pd.DataFrame(bookings)

        st.dataframe(
            df,
            use_container_width=True
        )

        selected_id = st.selectbox(
            "Select booking for invoice",
            df["Booking ID"].tolist()
        )

        booking = next(
            item for item in bookings
            if item["Booking ID"] == selected_id
        )

        invoice = f"""

EV CHARGEHUB
SIMULATED INVOICE

Booking ID: {booking['Booking ID']}
Customer: {booking['Customer']}
Vehicle: {booking['Vehicle']}
Station: {booking['Station']}
Date: {booking['Date']}
Time: {booking['Time']}

Energy: {booking['Energy (kWh)']} kWh
Price per kWh: ₹{booking['Price (₹)']}
Estimated total: ₹{booking['Estimated Bill (₹)']}

Status: {booking['Status']}

This is a simulated invoice, not a payment receipt.
"""

        st.text(invoice)

        st.download_button(
            "Download Invoice",
            data=invoice,
            file_name=f"{selected_id}_invoice.txt",
            mime="text/plain"
        )

    else:

        st.info(
            "No bookings yet. Create your first booking."
        )

except Exception:

    st.error(
        "Unable to retrieve bookings. "
        "Check the database configuration."
    )


elif page == "Admin Dashboard":

st.header("📊 Admin Dashboard")

try:
    bookings = get_all_bookings()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Stations",
        len(stations)
    )

    col2.metric(
        "Total Bookings",
        len(bookings)
    )

    total_value = sum(
        item["Estimated Bill (₹)"]
        for item in bookings
    )

    col3.metric(
        "Estimated Booking Value",
        f"₹{total_value:.2f}"
    )

    st.subheader("Charging Station Details")

    st.dataframe(
        pd.DataFrame(stations),
        use_container_width=True
    )

    st.subheader("Recent Bookings")

    if bookings:

        st.dataframe(
            pd.DataFrame(bookings),
            use_container_width=True
        )

    else:

        st.info("No bookings have been created yet.")

except Exception:

    st.error(
        "Unable to load dashboard data. "
        "Check your database configuration."
    )



st.divider()

st.caption(
"EV ChargeHub | Smart EV Charging Station Management System"
)
