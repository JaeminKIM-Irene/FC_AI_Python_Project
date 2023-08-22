from module.buddy_search import search
from module.buddy_weather import weather
from module.buddy_air import air
from module.buddy_game import word_game
import speech_recognition as sr
from module.voice_text import speak
import re

r = sr.Recognizer()
mic = sr.Microphone()

with mic as source :
    while True :
        # "친구야"라고 불러야 반응
        try :
            print(">>>")
            audio = r.listen(source)
            calling = r.recognize_google(audio, language='ko-KR')
        
            if calling == '친구야' :
                print('''
                1. ~ 검색
                2. ~ 날씨
                3. ~ 미세먼지
                4. 게임
                5. 종료
                ''')
                speak("무엇을 도와드릴까요?")
                print(">>>")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                try : 
                    
                    command = r.recognize_google(audio, language='ko-KR')
                    if '검색' in command :
                        keyword = command.split('검색')[0].strip()
                        if keyword == '' :
                            speak("검색 키워드와 함께 말씀해주세요")
                        else :
                            search(keyword)
                    elif '날씨' in command :
                        place = command.split('날씨')[0]
                        place = place.replace('오늘','').strip()
                        if place == '' :
                            weather('수내동')
                        else :
                            weather(place)
                    elif '미세먼지' in command or '미세 먼지' in command:
                        place = re.split(r'미세먼지|미세 먼지', command)[0]
                        place = place.replace('오늘','').strip()
                        if place == '' :
                            air('경기', '수내동')
                        else :
                            region = place.split()
                            air(region[0], region[1]) if len(region) == 2 else air(region[0], "")
                    elif '게임' in command :
                        word_game()
                    elif command == '종료' :
                        speak("종료합니다")
                        break
                    else :
                        speak("제공하지 않는 서비스입니다. 다시 말해주세요.")
                except :
                    speak('다시 말해주세요')

        # 미세한 소리에도 unknownvalueError가 지속적으로 발생하여 continue처리 하였습니다.
        except sr.UnknownValueError:
            continue
        except sr.RequestError:
            speak('다시 말해주세요')
        except sr.WaitTimeoutError:
            speak('다시 말해주세요')
