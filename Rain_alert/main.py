import os
from twilio.rest import Client
import requests
from dotenv import load_dotenv
from geopy.geocoders import Nominatim


def get_current_gps_coordinates():

    # Initialize the Nominatim geocoder with a user agent for identification
    geolocator = Nominatim(user_agent="RainAlertSystem")

    # Prompt the user to enter a city name
    place = input("Enter city name: ")

    # Attempt to geocode the provided city name
    location = geolocator.geocode(place)

    # Check if the location was found and return the coordinates
    if location:
        return location.latitude, location.longitude

    # Return None if the location could not be found
    return None


def get_data(latitude, longitude, key):
    # Construct the API URL for fetching weather data
    api_url = f'https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={key}'

    # Send a GET request to the API
    response = requests.get(api_url)
    response.raise_for_status()  # Raise an error for bad responses

    # Parse the JSON response
    data = response.json()

    # Extract weather data and timestamps
    weather_data = [(dt['dt_txt'], dt['weather'][0]) for dt in data['list']]

    rain_times = []  # List to store rain information

    # Loop through the weather data to find clear weather
    for timestamp, weather in weather_data:
        if weather['main'].lower() == 'rain':
            rain_times.append((weather['description'], timestamp))
            # Stop after finding the first two entries
            if len(rain_times) >= 2:
                break

    # Return None if there is no upcoming rain information
    return rain_times if rain_times else None


def send_alert(data, account_sid, token, message_service_sid, cell_number):
    # Check if there is data available for alerting
    if data is not None:
        # Extract the time from the second data entry
        time = data[1][1].split()
        time_value = int(time[1].split(':')[0])  # Get the hour component

        # Determine if the time is in the AM or PM
        suffix = 'am' if time_value < 12 else 'pm'

        # Create the message text for the alert
        message_text = f"\n\nHi\nExpect {data[1][0]}\nOn {time[0]}\nAround {time[1]} {suffix}"

        # Initialize the Twilio client
        client = Client(account_sid, token)

        try:
            # Send the alert message using Twilio's messaging service
            message = client.messages.create(
                messaging_service_sid=message_service_sid,
                body=message_text,
                to=cell_number  # Replace with the recipient's phone number
            )
            if message.sid:  # Check if the message was sent successfully
                print(f"Notification sent to {cell_number}")
        except Exception as e:
            print(f"Failed to send message: {e}")  # Handle any errors in sending

    else:
        print("There is no upcoming rain.")  # Notify if there's no data


def main():
    # Load environment variables from a .env file
    load_dotenv()

    # Retrieve necessary credentials from environment variables
    ACCOUNT_SID = os.getenv('ACCOUNT_SID')
    AUTH_TOKEN = os.getenv('AUTH_TOKEN')
    API_KEY = os.getenv('API_KEY')
    MESSAGE_SERVICE_SID = os.getenv('MESSAGE_SERVICE_SID')
    CELL_NUMBER = os.getenv('CELL_NUMBER')


    # Get latitude and longitude of the current location
    coordinates = get_current_gps_coordinates()

    if coordinates is not None:
        latitude, longitude = coordinates  # Unpack latitude and longitude

        # Fetch weather data based on current location
        data = get_data(latitude, longitude, API_KEY)

        # Send an alert based on the fetched data
        send_alert(data, ACCOUNT_SID, AUTH_TOKEN, MESSAGE_SERVICE_SID,CELL_NUMBER)
    else:
        # Error message for location retrieval failure
        print("Error: couldn't retrieve your location. Please check your internet connection.")


if __name__ == "__main__":
    main()
