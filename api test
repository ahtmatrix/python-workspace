import requests

API_KEY = ""

# where to send the query
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# request user to input city
city = input("Enter a city name: ")


request_url = f"{BASE_URL}?q={city}&appid={API_KEY}"

response = requests.get(request_url)

# 200 means ok successful
if response.status_code == 200:
    data = response.json()

    print(data)
else:
    print("error occured.")
