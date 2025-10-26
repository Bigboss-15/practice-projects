import tkinter as tk
from tkinter import messagebox
from urllib import request, error, parse
import json

# Dictionary mapping continents to representative coordinates
CONTINENT_COORDINATES = {
    "Africa": {"latitude": 0.0, "longitude": 20.0},
    "Antarctica": {"latitude": -82.0, "longitude": 60.0},
    "Asia": {"latitude": 34.0, "longitude": 100.0},
    "Europe": {"latitude": 50.0, "longitude": 10.0},
    "North America": {"latitude": 40.0, "longitude": -100.0},
    "Oceania": {"latitude": -25.0, "longitude": 135.0},
    "South America": {"latitude": -20.0, "longitude": -60.0}
}

def get_continent_weather(continent):
    """
    Fetch weather data for a given continent
    Returns formatted weather information or error message
    """
    if not continent.strip():
        return "Please select a valid continent"
    
    # Check if continent is in our list
    if continent not in CONTINENT_COORDINATES:
        return f"Continent '{continent}' not found in our database"
    
    # Get coordinates for the continent
    coords = CONTINENT_COORDINATES[continent]
    lat = coords["latitude"]
    lon = coords["longitude"]
    
    # Get weather information
    weather_url = (f"https://api.open-meteo.com/v1/forecast?"
                  f"latitude={lat}&longitude={lon}"
                  f"&current_weather=true"
                  f"&timezone=auto")
    
    try:
        with request.urlopen(weather_url, timeout=10) as response:
            weather_data = json.loads(response.read().decode())
            current = weather_data["current_weather"]
            
            # Get weather description from weather code
            weather_description = get_weather_description(current['weathercode'])
            
            return (f"Continent: {continent}\n"
                   f"Temperature: {current['temperature']}°C\n"
                   f"Weather: {weather_description}\n"
                   f"Wind Speed: {current['windspeed']} km/h")
    except error.URLError as e:
        return "Network error: Please check your internet connection"
    except json.JSONDecodeError:
        return "Error: Invalid response from weather service"
    except Exception as e:
        return f"Error: {str(e)}"

def get_weather_description(weather_code):
    """Convert weather code to descriptive text"""
    weather_descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        95: "Thunderstorm"
    }
    return weather_descriptions.get(weather_code, f"Unknown ({weather_code})")

def on_submit():
    """Handle submit button click"""
    selected_continent = continent_var.get()
    if selected_continent:
        result = get_continent_weather(selected_continent)
        messagebox.showinfo("Weather Information", result)
    else:
        messagebox.showwarning("Selection Error", "Please select a continent")

# Create main window
root = tk.Tk()
root.title("Continent Weather App")
root.geometry("400x300")
root.resizable(False, False)

# Create and pack widgets
title_label = tk.Label(root, text="Continent Weather Forecast", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

instruction_label = tk.Label(root, text="Select a continent:")
instruction_label.pack(pady=5)

# Create dropdown for continent selection
continent_var = tk.StringVar()
continents = list(CONTINENT_COORDINATES.keys())
continent_dropdown = tk.OptionMenu(root, continent_var, *continents)
continent_dropdown.config(width=20, font=("Arial", 12))
continent_dropdown.pack(pady=10)

# Set default selection
continent_var.set(continents[0])

# Create button frame
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

submit_button = tk.Button(button_frame, text="Get Weather", command=on_submit, 
                         bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                         padx=10, pady=5)
submit_button.pack(side=tk.LEFT, padx=5)

# Add information about the app
info_label = tk.Label(root, text="Note: Shows weather at representative coordinates", 
                     font=("Arial", 9), fg="gray")
info_label.pack(pady=10)

# Add attribution
attribution = tk.Label(root, text="Powered by Open-Meteo", 
                      font=("Arial", 8), fg="gray")
attribution.pack(side=tk.BOTTOM, pady=5)

root.mainloop()