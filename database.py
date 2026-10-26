import streamlit as st
import uuid
from supabase import create_client


@st.cache_resource
def get_database():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]

    return create_client(url, key)


def create_booking(
    customer,
    vehicle,
    station,
    booking_date,
    booking_time,
    energy_kwh,
    price_per_kwh
):
    db = get_database()

    # UUID provides a highly collision-resistant booking ID.
    booking_id = f"EV-{uuid.uuid4().hex[:12].upper()}"

    estimated_bill = round(
        float(energy_kwh) * float(price_per_kwh),
        2
    )

    record = {
        "booking_id": booking_id,
        "customer": customer,
        "vehicle": vehicle,
        "station": station,
        "booking_date": str(booking_date),
        "booking_time": str(booking_time),
        "energy_kwh": float(energy_kwh),
        "price_per_kwh": float(price_per_kwh),
        "estimated_bill": estimated_bill,
        "status": "Booked"
    }

    # The database primary key rejects duplicate IDs.
    result = db.table("bookings").insert(record).execute()

    return booking_id, estimated_bill


def get_all_bookings():
    db = get_database()

    result = (
        db.table("bookings")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    bookings = []

    for row in result.data:
        bookings.append({
            "Booking ID": row["booking_id"],
            "Customer": row["customer"],
            "Vehicle": row["vehicle"],
            "Station": row["station"],
            "Date": row["booking_date"],
            "Time": row["booking_time"],
            "Energy (kWh)": float(row["energy_kwh"]),
            "Price (₹)": float(row["price_per_kwh"]),
            "Estimated Bill (₹)": float(row["estimated_bill"]),
            "Status": row["status"]
        })

    return bookings
