
import streamlit as st
from supabase import create_client
from uuid import uuid4

# =====================================
# SUPABASE CONNECTION
# =====================================

SUPABASE_URL = st.secrets["https://nkkdyxtkvrcnhguxepbs.supabase.co"]
SUPABASE_KEY = st.secrets["sb_publishable_FoHhPzAD7U-2g0daTKPOiQ_f16FIKme"]

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# =====================================
# CREATE BOOKING
# =====================================

def create_booking(
    customer,
    vehicle,
    station,
    booking_date,
    booking_time,
    energy,
    price
):
    booking_id = str(uuid4())[:8].upper()

    energy = float(energy)
    price = float(price)

    bill = energy * price

    booking_data = {
        "booking_id": booking_id,
        "customer": customer,
        "vehicle": vehicle,
        "station": station,
        "booking_date": str(booking_date),
        "booking_time": str(booking_time),
        "energy_kwh": energy,
        "price_per_kwh": price,
        "estimated_bill": round(bill, 2),
        "status": "Booked"
    }

    response = (
        supabase.table("bookings")
        .insert(booking_data)
        .execute()
    )

    if not response.data:
        raise Exception("Booking insert returned no data")

    return booking_id, round(bill, 2)


# =====================================
# GET ALL BOOKINGS
# =====================================

def get_all_bookings():

    response = (
        supabase.table("bookings")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    bookings = []

    for row in response.data:

        booking = {
            "Booking ID": row.get("booking_id"),
            "Customer": row.get("customer"),
            "Vehicle": row.get("vehicle"),
            "Station": row.get("station"),
            "Date": row.get("booking_date"),
            "Time": row.get("booking_time"),
            "Energy (kWh)": row.get("energy_kwh"),
            "Price (₹)": row.get("price_per_kwh"),
            "Estimated Bill (₹)": row.get("estimated_bill"),
            "Status": row.get("status"),
            "Created At": row.get("created_at")
        }

        bookings.append(booking)

    return bookings
