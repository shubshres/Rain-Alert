import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "http://api.openweathermap.org/data/2.5/onecall"
api_key = "YOUR API KEY HERE"
account_sid = "YOUR ACCOUNT SID HERE"
auth_token = "YOUR AUTH TOKEN HERE"

weather_params = {
    "lat": YOUR LATTITUDE HERE,
    "lon": YOUR LONGITUDE HERE,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's going to rain today! 🌧",
        from_='FROM NUMBER HERE',
        to='TO NUMBER HERE'
    )

# making sure message was sent successfully
print(message.status)
