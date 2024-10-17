import requests
import time
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine, Column, Float, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///weather_data.db')  # Use SQLite for simplicity
Session = sessionmaker(bind=engine)
session = Session()

# Weather data model
class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True)
    date = Column(String)
    avg_temp = Column(Float)
    max_temp = Column(Float)
    min_temp = Column(Float)
    condition = Column(String)

Base.metadata.create_all(engine)

# Constants
API_KEY = '08bb73cf460aa638d38ed76b86dabe33'  # Your OpenWeatherMap API key
CITY = 'Bhubaneswar'  # City to monitor
URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'  # Get temperature in Celsius

# Function to fetch weather data
def fetch_weather():
    response = requests.get(URL)
    data = response.json()
    print(data)  # Print the API response for debugging

    # Check for error in the response
    if data.get('cod') != 200:
        print(f"Error fetching weather data: {data.get('message')}")
        return None  # Return None or handle the error as needed

    return {
        'temperature': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'condition': data['weather'][0]['main'],
        'dt': data['dt']
    }


# Function to process and store weather data
def store_weather_data(data):
    date_str = time.strftime('%Y-%m-%d', time.localtime(data['dt']))
    weather_entry = WeatherData(date=date_str, avg_temp=data['temperature'],
                                 max_temp=data['temperature'], min_temp=data['temperature'],
                                 condition=data['condition'])
    session.add(weather_entry)
    session.commit()

# Function to plot average daily temperatures
def plot_avg_temp():
    results = session.query(WeatherData).all()
    if results:
        dates = [result.date for result in results]
        avg_temps = [result.avg_temp for result in results]
        
        plt.figure(figsize=(10, 5))
        plt.plot(dates, avg_temps, marker='o')
        plt.title('Average Daily Temperature in Bhubaneswar')
        plt.xlabel('Date')
        plt.ylabel('Average Temperature (°C)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid()
        plt.show()
    else:
        print("No data available for plotting.")

# Main execution loop
def main():
    while True:
        weather_data = fetch_weather()
        store_weather_data(weather_data)
        plot_avg_temp()
        time.sleep(300)  # Wait for 5 minutes before the next fetch

if __name__ == "__main__":
    main()
