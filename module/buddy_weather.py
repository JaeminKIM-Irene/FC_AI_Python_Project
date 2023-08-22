import requests
import json
import googlemaps
from module.voice_text import speak
from dotenv import load_dotenv
import os

def get_location (name) :
    load_dotenv()
    gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_KEY'))
    try : 
        geocode_result = gmaps.geocode((name), language='ko')[0].get('geometry')
        lat = geocode_result['location']['lat']
        lon = geocode_result['location']['lng']
    except :
        speak("해당 지역의 날씨를 찾을 수 없습니다.")
        lat = 0
        lon = 0
    return lat, lon

def weather(name) :
    lat, lon = get_location(name)
    if lat and lon :
        res = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true')
        data = json.loads(res.text)
        text = f"현재 {name}은(는) {data['current_weather']['temperature']}도 입니다"
        print(text)
        speak(text)