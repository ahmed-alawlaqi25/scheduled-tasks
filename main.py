import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
api_key = os.environ.get("API_KEY")

weather_parms ={
    "lat": 37.5774,
    "lon": 43.7368,
    "cnt": 4,
    "appid": api_key,
}

response = requests.get(OWM_Endpoint, params=weather_parms)
response.raise_for_status()
weather_data = response.json()

will_rain = False
for hour_data in weather_data['list']:
    condition_code = hour_data['weather'][0]['id']
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella",
        from_="YOUR TWILIO VIRTUAL NUMBER",
        to="YOUR TWILIO VERIFIED REAL NUMBER",
    )
    print(message.status)

