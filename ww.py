
import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import ttkbootstrap

# Function to get weather information from OpenWeatherMap API
def get_weather(city):
    API_key = "1b2f8c4cbcbd0ee0ce628c4130e28dc2"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None

    # Parse the response JSON to get weather information
    weather = res.json()
    print("Weather response:", weather)  # Add this line for debugging
    try:
        icon_id = weather['weather'][0]['icon']
        temperature = weather['main']['temp'] - 273.15
        description = weather['weather'][0]['description']
        city = weather['name']
        country = weather['sys']['country']
        timezone = weather['timezone']

        # Get dust information
        lat = weather['coord']['lat']
        lon = weather['coord']['lon']
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_key}"
        res_dust = requests.get(url)

        dust = res_dust.json()
        pm_25 = dust['list'][0]['components']['pm2_5']
        pm_10 = dust['list'][0]['components']['pm10']
        c0 = dust['list'][0]['components']['co']

        # Get the icon URL and return all the weather information
        icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
        
        # Calculate local time based on timezone
        local_time = datetime.utcnow() + timedelta(seconds=timezone)
        local_time_str = local_time.strftime("%H:%M")

        return (icon_url, temperature, description, city, country, local_time_str, pm_25, pm_10, c0)
    except KeyError:
        messagebox.showerror("Error", "Unable to retrieve weather information")
        return None

# Function to search weather for a city
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    icon_url, temperature, description, city, country, local_time_str, pm_25, pm_10, c0 = result

    location_label.configure(text=f"{city}, {country}")
    timezone_label.configure(text=f"Local Time: {local_time_str}")
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    temperature_label.configure(text=f"Temperature: {temperature:.1f} °C")
    description_label.configure(text=f"Description: {description}")

    # Update labels for dust information
    pm_25_label.configure(text=f"PM2.5: {pm_25} µg/m³")
    pm_10_label.configure(text=f"PM10: {pm_10} µg/m³")
    c0_label.configure(text=f"CO: {c0} µg/m³")

# Create the main window
root = ttkbootstrap.Window(themename="morph")
root.title("Weather App")
root.geometry("400x520")

# Create an entry widget -> to enter the city name
city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

# Create a button widget -> to search for the weather information
search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

# Create a label widget -> to show the city/country name
location_label = tk.Label(root, font=("Baloo Bhaijaan", 25))
location_label.pack()

timezone_label = tk.Label(root, font=("Baloo Da 2", 20))
timezone_label.pack()

# Create a label widget -> to show the weather icon
icon_label = tk.Label(root)
icon_label.pack()

# Create a label widget -> to show the temperature
temperature_label = tk.Label(root, font=("Baloo Da 2", 20))
temperature_label.pack()

# Create a label widget -> to show the weather description
description_label = tk.Label(root, font=("Baloo Da 2", 20))
description_label.pack()

# Create a label widget -> to show the pm2.5
pm_25_label = tk.Label(root, font=("Baloo Da 2", 20))
pm_25_label.pack()

# Create a label widget -> to show the pm10
pm_10_label = tk.Label(root, font=("Baloo Da 2", 20))
pm_10_label.pack()

# Create a label widget -> to show the co
c0_label = tk.Label(root, font=("Baloo Da 2", 20))
c0_label.pack()

root.mainloop()