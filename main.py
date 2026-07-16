import requests

def get_location_data(city):
    
    try:
        response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search?name=" + city,
            timeout=10
        )
        
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return None, "connection_error"
    
    response_data = response.json()

    if "results" not in response_data:
        return None, "city_not_found"
    
    data = response_data['results'][0]

    latitude = data['latitude']
    longitude = data['longitude']
    country = data['country']
    city_name = data['name']

    return (city_name, country, latitude, longitude), None

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
        return None, "connection_error"
    
    current = response.json()['current']

    weather_data = (    
    current['temperature_2m'],
    current['relative_humidity_2m'],
    current['wind_speed_10m']
    )

    return weather_data, None

def connection_error():
    print("Could not connect to the weather service. Please try again later.")

def main():

    city = input("\nEnter a city name: ").strip().title()

    location_data, error = get_location_data(city)

    if error == "connection_error":
        connection_error()
        return
    elif error == "city_not_found":
        print(f"City not found.")
        return
    
    city_name, country_name, latitude, longitude = location_data

    weather_data, error = get_weather(latitude, longitude)

    if error == "connection_error":
        connection_error()
        return

    temperature, humidity, wind_speed = weather_data

    print(f"======================================")
    print(f"            WEATHER REPORT            ")
    print(f"======================================")
    print(f"\nCity: {city_name}")
    print(f"Country: {country_name}")
    print(f"\nLatitude: {latitude:.4f}")
    print(f"Longitude: {longitude:.4f}")
    print(f"\nCurrent temperature: {temperature}°C")
    print(f"Current relative humidity: {humidity}%")
    print(f"Current wind speed: {wind_speed} km/h\n")


main()