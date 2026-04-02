import requests
import json 
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")

cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata","Hyderabad", "Pune", "Ahmedabad", "Surat", "Jaipur"]

all_data = []

for city in cities:
    print(city)    
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"    
    
    try:
        response = requests.get(url)

        if response.status_code == 404:
            print(f"City {city} not found.")
            continue

        if response.status_code == 401:
            print("Invalid API key.")
            break

        if response.status_code == 200:
            data = response.json()

            temp_c = data['main']['temp'] - 273.15   
            temp_c = str(round(temp_c,2))+" C"
            time = datetime.fromtimestamp(data["dt"])          

            weather_info = {
                "city": city,
                "temperature": temp_c,
                "humidity": data["main"]["humidity"],
                "weather": data["weather"][0]["main"],
                "time": str(time)
            }        

            all_data.append(weather_info)

        else:
            print("Error:", city)

    except Exception as e:
        print("Something went wrong for", city)
        print(e)

with open("weather_data.json","w") as f:
    json.dump(all_data,f,indent=4)  

print("Data saved to weather_data.json")