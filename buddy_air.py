import requests
import json

from voice_text import speak
from dotenv import load_dotenv
import os

# 미세먼지 수치와 등급이 제대로 들어와있는지 확인
def valid_data(data) :
    if (data['pm10Value'] != None and data['pm10Value'] != '-') and (data['pm10Grade'] != None and data['pm10Grade'] != '-') :
        station = data['stationName']
        val = data['pm10Value']
        grade = data['pm10Grade']
        return 1, station, val, grade
    else :
        return 0, "", -1, -1

def air(city, station) :
    load_dotenv()
    if city[-1] == '시' or city[-1] == '도' :
        city = city[:-1]
    params = {
        'serviceKey': os.environ.get('AIR_KEY'),
        'returnType': 'json',
        'numOfRows': '100',
        'pageNo': '1',
        'sidoName': f'{city}',
        'ver': '1.0',
    }

    try : 
        res = requests.get('http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty', params=params)
        data = json.loads(res.text)['response']['body']['items']
        # 세부 지역이 주어지지 않은 경우
        if station == "" :
            for d in data :
                flag, station, val, grade = valid_data(d)
                if flag == 1 : break
                # 모든 정보가 비정상적일 경우
                if d == data[-1] :
                    speak("현재 정상적으로 미세먼지 정보를 불러올 수 없습니다. 나중에 다시 시도해주세요.")
                    return
        # 세부 지역이 주어진 경우
        else :
            for d in data :
                if d['stationName'] == station :
                    flag, station, val, grade = valid_data(d)
                    break
                # 일치하는 stationName을 찾을 수 없는 경우
                if d == data[-1] :
                    speak("해당 지역의 미세먼지 정보는 찾을 수 없습니다. 지역 이름이 정확한지 확인해주세요.")
                    return
        if flag == 1 : 
            text = f"{city} {station}의 미세먼지 수치는 {val}이고 {grade}등급 입니다."
        else :
            text = "현재 정상적으로 미세먼지 정보를 불러올 수 없습니다. 나중에 다시 시도해주세요."
        print(text)
        speak(text)
    except :
        speak("해당 지역의 미세먼지 정보는 찾을 수 없습니다.")