import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
api_key = os.getenv("94883ee50707050a662509a66ec8d1aa")

# Function to fetch weather data
def get_weather_forecast(location, months=1):
    base_url = "http://api.openweathermap.org/data/2.5/forecast/daily"
    num_days = months * 30  # Approximate number of days for the forecast

    params = {
        'q': location,
        'cnt': num_days,
        'appid': api_key,
        'units': 'metric'
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        forecast_data = data['list']
        forecast = [{
            "date": datetime.fromtimestamp(day['dt'], timezone.utc),  # Updated to use timezone-aware datetime
            "temp": day['temp']['day'],
            "weather": day['weather'][0]['description']
        } for day in forecast_data]

        return pd.DataFrame(forecast)
    else:
        st.error(f"Error fetching data: {data.get('message', 'Failed to fetch weather data')}")
        return pd.DataFrame()

# Crop recommendation function
def crop_recommendations(forecast_df):
    # Sample recommendations based on temperature
    recommendations = []
    for _, row in forecast_df.iterrows():
        if 20 <= row["temp"] <= 30:
            recommendations.append("Tomatoes, Peppers")
        elif row["temp"] < 20:
            recommendations.append("Lettuce, Spinach")
        else:
            recommendations.append("Watermelon, Cucumber")

    forecast_df['Recommended Crops'] = recommendations
    return forecast_df

# Streamlit dashboard function
def display_dashboard(forecast_df):
    st.title("Weather-Based Crop Recommendation System")
    st.write("Location: Pretoria")

    # Display the weather forecast data
    st.write("Weather Forecast for the Next Months:")
    st.dataframe(forecast_df)

    # Plot temperature trends
    fig, ax = plt.subplots()
    ax.plot(forecast_df['date'], forecast_df['temp'], color='blue', marker='o')
    ax.set_title("Temperature Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    st.pyplot(fig)

    # Display crop recommendations
    st.write("Crop Recommendations based on Weather:")
    for i, row in forecast_df.iterrows():
        st.write(f"{row['date'].strftime('%Y-%m-%d')}: {row['Recommended Crops']}")

# Main execution
location = "Pretoria"  # You can change this to any location
forecast_df = get_weather_forecast(location, months=1)
if not forecast_df.empty:
    forecast_df = crop_recommendations(forecast_df)
    display_dashboard(forecast_df)
else:
    st.write("No forecast data available.")

