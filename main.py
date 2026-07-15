import requests

def get_location_data(city):
    
    try:
        response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search?name=" + city,
            timeout=10
        )
        
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return "connection_error"
    
    response_data = response.json()

    if "results" not in response_data:
        return None
    
    data = response_data['results'][0]

    latitude = data['latitude']
    longitude = data['longitude']
    country = data['country']
    city_name = data['name']

    return city_name, country, latitude, longitude

def get_weather(latitude, longitude):
    try:
        response = requests.get(
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}"
            f"&longitude={longitude}"
            f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m",
            timeout=10
        )
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return None
    
    current = response.json()['current']

    return (    
    current['temperature_2m'],
    current['relative_humidity_2m'],
    current['wind_speed_10m']
    )

def main():

    city = input("Enter a city name: ").strip().title()

    location_data = get_location_data(city)

    if location_data is None:
        print(f"City not found.")
        return

    if location_data == "connection_error":
        print("Could not connect to the weather service. Please try again later.")
        return

    city_name, country_name, latitude, longitude = location_data

    weather = get_weather(latitude, longitude)

    if weather is None:
        print("Could not retrieve weather data. Please try again later.")
        return

    temperature, humidity, wind_speed = weather

    print(f"======================================")
    print(f"            WEATHER REPORT            ")
    print(f"======================================")
    print(f"\nCity: {city_name}")
    print(f"Country: {country_name}")
    print(f"\nLatitude: {latitude:.4f}")
    print(f"Longitude: {longitude:.4f}")
    print(f"\nCurrent temperature: {temperature}°C")
    print(f"Current relative humidity: {humidity}%")
    print(f"Current wind speed: {wind_speed} km/h")


main()