import requests
from geopy.geocoders import Nominatim

def get_weather(myCity):
    '''
    Returns TEMPERATURE and SKY CONDITION from myCity input
    '''

    myCity = "Pato Branco, PR"
    geolocator = Nominatim(user_agent="samantha")
    location = geolocator.geocode(myCity)
    weather_apikey = 'ce11202252e8cc8a4fc0ded88a90dcaf'
    query = 'https://api.openweathermap.org/data/2.5/onecall?lat='+ str(location.latitude) +'&lon='+ str(location.longitude) +'&exclude=hourly,daily&appid=' + weather_apikey

    print("Iniciando requisição de CLIMA.")
    resp = requests.get(query)

    if resp.status_code != 200:
        # This means something went wrong.
        print("\nErro 200!")

    print("Requisição de CLIMA OK.")
    temperature = resp.json()['current']['temp']-273.15
    temperature_feelslike = resp.json()['current']['feels_like']-273.15
    humidity = resp.json()['current']['humidity']
    skyCondition = resp.json()['current']['weather'][0]['main']
    uvi = resp.json()['current']['uvi']

    return temperature, temperature_feelslike, humidity, skyCondition, uvi
    
