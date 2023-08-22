import requests
import json
import random
import re

import speech_recognition as sr
from voice_text import speak
from dotenv import load_dotenv
import os

def comp_search(letter) :
    load_dotenv()
    word_list = []
    params = {
        'key': os.environ.get('KOR_KEY'),
        'q': letter,
        'req_type': 'json',
        'start': 1,
        'num': 100,
        'advanced' : 'y',
        'method' : 'start',
        'type1' : 'word',
        'type2' : ['native', 'chinese', 'loanword'],
        'type3' : 'general',
        'pos' : [1],
    }
    try : 
        res = requests.get('http://opendict.korean.go.kr/api/search', params = params)
        data = json.loads(res.text)['channel']['item']

        for d in data :
            new_d = re.sub(r"[^가-힣]", "", d['word'])
            if len(new_d) >= 2 :
                word_list.append(new_d)
        
        word_choice = random.choice(word_list)
        print(word_choice)
        speak(word_choice)

        return word_choice[-1]
    except :
        speak("현재 게임 진행이 불가합니다") 

def user_search(word) :
    params = {
        'key': '9EEB85230FA3889F1026BDCF9E0FC50C',
        'q': word,
        'req_type': 'json',
        'start': 1,
        'num': 10,
        'advanced' : 'y',
        'method' : 'exact',
        'type1' : 'word',
        'type2' : ['native', 'chinese', 'loanword'],
        'pos' : [1],
    }
    try : 
        res = requests.get('http://opendict.korean.go.kr/api/search', params = params)
        data = json.loads(res.text)['channel']['item']
    except :
        speak("현재 게임 진행이 불가합니다") 
        return

    if data != [] :
        new_d = re.sub(r"[^가-힣]", "", data[0]['word'])
        if new_d == word :
            print(word)
            return word[-1]
    else :
        speak(f"해당 단어 '{word}'는 존재하지 않습니다. 다시 말씀해주세요.")
  
def user_check(start_letter, user) : 
    if start_letter == '원하는 글자' :
        if len(user) >= 2 :
            start_letter = user_search(user)
        else : 
            speak("2글자 이상 단어로 말씀해주세요")
            return
    else :
        if len(user) >= 2 and user[0] == start_letter :
            start_letter = user_search(user)
        else : 
            speak("조건에 맞는 단어로 다시 말씀해주세요")
            return
    return start_letter

def word_game () :
    # -- 게임 룰 --
    # 총 5판 진행 후 비기면 유저의 승리. 게임이 종료된다.
    # 유저에게는 다시 말할 기회가 한 턴당 3번 주어진다.
    # 3번 동안 조건을 충족하는 단어를 얘기하지 못하는 경우 패배. 게임이 종료된다.

    r = sr.Recognizer()
    mic = sr.Microphone()
    start_letter = '원하는 글자'

    print("--- 게임 시작 ---")
    for _ in range(3) :
        # 유저는 총 3번의 기회를 갖는다
        for i in range(3) :
            try : 
                print(f"'{start_letter}'(으)로 시작하는 단어를 말씀해주세요 >>>")
                speak(f"'{start_letter}'(으)로 시작하는 단어를 말씀해주세요 >>>")
                with mic as source :
                    print(">>>")
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                user = r.recognize_google(audio, language = 'ko-KR')
                temp = user_check(start_letter, user)
                if temp != None :
                    start_letter = temp
                    break
            except :
                speak('다시 말해주세요')
            if i == 2 :
                speak("세턴 안에 말하지 못했습니다. 패배.")
                return

        start_letter = comp_search(start_letter)
        if start_letter == None :
            return

    speak("승리하였습니다. 게임을 종료합니다.")
