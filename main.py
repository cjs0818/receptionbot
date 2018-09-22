# -*- coding: utf-8 -*-

import json
import time

from chatbot.danbee import Danbee   # Chatbot platform: Danbee.ai
from tts.naver_tts import NaverTTS  # TTS: NaverTTS
from stt.gspeech import Gspeech     # STT: Google Cloud Speech



def speech_ui(stt_enable=1, tts_enable=1):

    # --------------------------------
    # Start Chatbot with Danbee API
    # --------------------------------
    user_key = 'DeepTasK'
    chatbot_id = 'c54e4466-d26d-4966-af1f-ca4d087d0c4a'

    chat = Danbee(chatbot_id)


    # --------------------------------
    # Create NaverTTS Class
    tts = NaverTTS(0,-1)    # Create a NaverTTS() class from tts/naver_tts.py
    #tts.play("안녕하십니까?")


    if stt_enable == 1:
        # 음성인식인 경우 무한 loop
        flag = True
        gsp = Gspeech()
    else:
        # 음성인식 아닌 경우, 테스트 query에 대해 문장 단위로 테스트
        query = ["안녕",
                 "사람이요",
                 "최종석 박사님을 만나러 왔어요",
                 "아나스타샤를 찾으러 왔어요",
                 "홍길동님을 찾으러 왔어요",
                 "여진구 박사님이요",
                 "끝내자"
                 ]
        q_count = len(query)
        iter = 0
        flag = iter < q_count




    while flag:

        # 음성 인식 될때까지 대기 한다.
        try:
            if stt_enable == 1:
                flag = True
                stt = gsp.getText()
            else:
                iter = iter + 1
                flag = iter < q_count
                stt = query[iter-1]

            #if stt is None:
            #    break
            if stt is not None:
                print(stt)

            # time.sleep(0.01)
            if (u'끝내자' in stt):
                # -------------------------------
                # Event API test
                event = {
                    #"what": "Human is approaching",
                    "what": "Human is disappearing",
                    "who": "최종석"
                }
                res = event_api(event, user_key)
                # print(json.dumps(res, indent=4, ensure_ascii=False))
                message = res['responseSet']['result']['result'][0]['message']  # <- danbee json 포맷 분석 결과
                # -------------------------------
                break


            print("--------")
            content = stt
            res = chat.get_answer_danbee(content, user_key)
            message = res['responseSet']['result']['result'][0]['message']   # <- danbee json 포맷 분석 결과

            # -------------------------------
            # TTS 하는 동안 STT 일시 중지 --
            if stt_enable == 1:
                gsp.pauseMic()


            # ===============================
            # TTS
            if tts_enable == 1:
                tts.play(message)
            # -------------------------------



            try:
                name1 = res['responseSet']['result']['parameters']['person_to_visit']
            except Exception as e:
                pass

            try:
                name2 = res['responseSet']['result']['parameters']['sysany']
            except Exception as e:
                pass

            if(len(name1)>0):
                name = name1
            elif(len(name2)>0):
                name = name2


            try:
                #name = res['responseSet']['result']['parameters']['person_to_visit']   # <- danbee json 포맷 분석 결과
                # ------------------------
                # 최종석 박사 -> 최종석
                # 최종석 -> 최종석
                # ------------------------
                name = name.split()
                name = name[0]
                if(len(name) > 0):
                    # ------------------------
                    # getting information of person(name) from database
                    # ------------------------
                    kind_of_guide = 'person'
                    db = chat.get_datatbase(kind_of_guide)
                    # json_data = json.dumps(db, indent=4, ensure_ascii=False)

                    print('============= print from internal process ==================')

                    # ------------------------
                    # database에 해당 name의 사람이 있으면 그 사람의 information을 갖고 오고,
                    # ''     ''      ''     ''  없으면 ERROR를 갖고 온다.
                    # ------------------------
                    try:
                        info = db[name]
                        try:
                            room_num = info["room#"]
                            msg = name + "님은 " + room_num + "호 에 계시며, 자세한 정보는 다음과 같습니다."
                        except:
                            msg = name + "님의 정보는 다음과 같습니다."
                        '''
                        info = {
                            "name": "최종석",
                            "information": {
                                "center": "지능로봇연구단",
                                "room#": "8402",
                                "phone#": "5618",
                                "e-mail": "cjs@kist.re.kr"
                            }
                        }
                        '''
                        # print('   information about ', name, ': ', json.dumps(info, indent=4, ensure_ascii=False))
                    except:
                        msg = "죄송합니다만, KIST 국제협력관에서 " + name + "님의 정보를 찾을 수 없습니다."
                        info = 'ERROR'

                    answer = {
                        'name': name,
                        'information': info
                    }
                    print(msg)
                    # ===============================
                    if tts_enable == 1:
                        tts.play(msg)
                    # -------------------------------
                    print(json.dumps(answer, indent=4, ensure_ascii=False))
                    print (info)

            except Exception as e:
                pass


            time.sleep(0.01)
            # -------------------------------
            # STT 재시작
            if stt_enable == 1:
                gsp.resumeMic()


            print("      --")
        except Exception as e:
            if stt_enable == 1:
                # 구글 음성인식기의 경우 1분 제한을 넘으면 오류 발생 -> 다시 클래스를 생성시킴
                del gsp
                gsp = Gspeech()
            pass




#----------------------------------------------------
# 메인 함수
#----------------------------------------------------
if __name__ == '__main__':

    stt_enable = 0  # 0: Disable speech recognition (STT), 1: Enable it
    tts_enable = 0  # 0: Disable speech synthesis (TTS),   1: Enable it

    speech_ui(stt_enable, tts_enable)
    #web_request()
