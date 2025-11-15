
import streamlit as st
import requests
import geocoder
import json
import pandas as pd
import datetime
from weather_db import init_db, save_weather_data, get_all_records, update_record, delete_record



# Initialize the database
init_db()
# 🌡️ Unit toggle
unit = st.radio("Choose temperature unit:", ["°C", "°F"], key="unit_selector")
unit_key = "temp_c" if unit == "°C" else "temp_f"

# 📍 Location input
use_auto = st.checkbox("Use my current location", value=False, key="use_auto_location")
location = st.text_input("📍 Enter location", key="manual_location_input")

@st.cache_data
def get_current_weather(location, unit):
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}"
    response = requests.get(url)
    return response.json()

@st.cache_data
def get_forecast(location, unit):
    url = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days=5"
    response = requests.get(url)
    return response.json()


 # 🧾 Fetch saved records from DB
try:
    records = get_all_records()
    if records:
        df = pd.DataFrame(records, columns=["ID", "Location", "Start Date", "End Date", "Temperature Data", "Timestamp"])
        st.subheader("📋 Saved Weather Records")
        st.dataframe(df)
    else:
        st.info("No records found yet.")
except Exception as e:
    st.error("⚠️ Could not load saved records.")
    st.write(e)

    st.subheader("🗑️ Delete a Record")

# Get all records again
records = get_all_records()

# Extract IDs for dropdown
record_ids = [str(row[0]) for row in records]  # row[0] is the ID

if record_ids:
    selected_id = st.selectbox("Select record ID to delete:", record_ids, key="delete_selector")
    if st.button("Delete Record"):
        try:
            delete_record(int(selected_id))
            st.success(f"✅ Record {selected_id} deleted successfully!")
        except Exception as e:
            st.error("⚠️ Failed to delete record.")
            st.write(e)
else:
    st.info("No records available to delete.")


# 🔑 Replace with your actual WeatherAPI key
API_KEY = "e256ec43b6d54cb09a7171400251411"
BASE_URL = "https://api.weatherapi.com/v1"

# 📍 Auto-detect location
def get_auto_location():
    g = geocoder.ip('me')
    return g.city if g.city else "Nairobi"

# 📦 Fetch current weather
@st.cache_data
def get_current_weather(location, unit):
    url = f"{BASE_URL}/current.json?key={API_KEY}&q={location}"
    response = requests.get(url)
    st.write("Status Code:", response.status_code)
    st.write("Raw Response:", response.text)
    return response.json()


# 📦 Fetch 5-day forecast
@st.cache_data
def get_forecast(location, unit):
    url = f"{BASE_URL}/forecast.json?key={API_KEY}&q={location}&days=5"
    response = requests.get(url)
    st.write("Status Code:", response.status_code)
    st.write("Raw Response:", response.text)
    return response.json()



# 🎨 Streamlit UI
st.set_page_config(page_title="Weather App", page_icon="⛅")
st.title("🌍 Real-Time Weather App")
st.write("Enter a location or use your current location to get weather updates.")

# 🌡️ Unit toggle
unit = st.radio("Choose temperature unit:", ["°C", "°F"])
unit_key = "temp_c" if unit == "°C" else "temp_f"

# 📍 Location input
use_auto = st.checkbox("Use my current location", value=False)
location = get_auto_location() if use_auto else st.text_input("📍 Enter location", placeholder="e.g. Nairobi, 10001, Eiffel Tower")

if location:
    current = None
    forecast = None

    try:
        current = get_current_weather(location, unit)
        forecast = get_forecast(location, unit)

        # 🌡️ Current Weather
        st.subheader("Current Weather")
        icon_url = "https:" + current['current']['condition']['icon']
        st.image(icon_url, width=100)
        st.write(f"**{current['location']['name']}, {current['location']['country']}**")
        st.write(f"🌡️ Temperature: {current['current'][unit_key]}{unit}")
        st.write(f"💨 Wind: {current['current']['wind_kph']} kph")
        st.write(f"🌥️ Condition: {current['current']['condition']['text']}")

        # 📅 5-Day Forecast
        st.subheader("5-Day Forecast")
        for day in forecast['forecast']['forecastday']:
            st.markdown(f"### {day['date']}")
            st.image("https:" + day['day']['condition']['icon'], width=80)
            st.write(f"🌡️ Max: {day['day']['maxtemp_c']}°C | Min: {day['day']['mintemp_c']}°C")
            st.write(f"🌥️ {day['day']['condition']['text']}")
            st.write("---")

    except Exception as e:
        st.error("⚠️ Could not fetch weather data. Please check the location or API key.")
        st.write(e)

    # ✅ Only run this if both are defined
    today = datetime.date.today()
    if current is not None and forecast is not None:
        st.markdown("✅ DEBUG: Calendar block reached")
        st.subheader("📅 Save Weather Data")
        start_date = st.date_input("Start Date", key="start_date_picker_1")
        end_date = st.date_input("End Date", key="end_date_picker_2")

        if st.button("Save to Database", key="save_button"):
            if start_date > end_date:
                st.error("⚠️ Start date must be before end date.")
            elif start_date == end_date:
                st.warning("⚠️ Start date and end date are the same. Do you want to save just one day?")
            else:
                weather_data = {
                    "current": current,
                    "forecast": forecast
                }
                save_weather_data(location, str(start_date), str(end_date), weather_data)
                st.success("✅ Weather data saved successfully!")

with st.sidebar:
    st.markdown("**Built by Sylvia Karanja** 💙")
    with st.expander("ℹ️ About PM Accelerator"):
        st.markdown("""
        **PM Accelerator** is a product management training and mentorship program.  
        Learn more on their [LinkedIn page](https://www.linkedin.com/company/product-manager-accelerator).
        """)