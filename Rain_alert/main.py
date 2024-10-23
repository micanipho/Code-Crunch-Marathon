import os

from twilio.rest import Client
import requests
import geocoder
from dotenv import load_dotenv

# TODO: retrieve user's location

def get_current_gps_coordinates():
    g = geocoder.ip('me') # this function is used to find the current information using our IP Add
    if g.latlng is not None:  # g.latlng tells if the coordinates are found or not
        return g.latlng
    else:
        return None

# TODO: detect rain forecast
# TODO: if there is an upcoming rain , send alert to user via an sms

def main():

    load_dotenv()

    ACCOUNT_SID = os.getenv('ACCOUNT_SID')
    AUTH_TOKEN = os.getenv('AUTH_TOKEN')
    API_KEY = os.getenv('API_KEY')

    # get latitude and longitude of current location
    coordinates = get_current_gps_coordinates()
    if coordinates is not None:
        latitude, longitude = coordinates
        api_url = f'https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={API_KEY}'

        response = requests.get(api_url)
        data = response.json()

        weather = [(dt['dt_txt'],dt['weather']) for dt in data['list']]


        rain_times = []

        for unit in weather:
            weather_description = unit[1][0]['main']
            time_of_weather = unit[0]
            if weather_description.lower() == 'clear':
                rain_times.append((unit[1][0]['description'], time_of_weather))
                break

        if len(rain_times) > 0:
            message_text = f"\n\nHi\nExpect {rain_times[0][0]}\nOn {rain_times[0][1]}"



            client = Client(ACCOUNT_SID, AUTH_TOKEN)
            message = client.messages.create(
                messaging_service_sid='MGfd7b4283f679fe927050c553e395cafd',
                body=message_text,
                to='+27636639970'
            )
            print(message.sid)
        else:
            print("No rain detected in the upcoming 5 days")

    else:
        print("Error: couldn't retrieve your location, check if you're connected to the internet.")

if __name__ == "__main__":
    main()
