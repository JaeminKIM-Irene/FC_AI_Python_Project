import requests
import json
import googlemaps
from voice_text import speak

def get_location (name) :
    gmaps = googlemaps.Client(key='AIzaSyBt7mfOS_H4hXIGE6N3fX8PR48IR5Rddog')
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