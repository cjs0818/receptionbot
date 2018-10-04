# -*- coding: utf-8 -*-

import requests
import json
import csv

import gspeech
import time

import os
import sys
import urllib.request

# Custom module
from tts.naver_tts import NaverTTS  # tts


#------------------
# Sound player
#
#    Linux  -> use cvlc :
#       sudo apt-get install vlc
#    OSX -> use playsound :
#       pip3 install pyobjc
#       pip3 install playsound


# Install
#       pip3 install pyobjc
#       pip3 install playsound
import subprocess
os_name = subprocess.check_output('uname', shell=True)
os_name = str(os_name)
if(os_name.find('Darwin') >= 0):
    from playsound import playsound  # For OSX
#------------------


def print_kor(text):
    #print(json.dumps(text, indent=4, ensure_ascii=False))
    print(text)


def event_api(event, user_key):
    data_send = {
        'chatbot_id': 'c54e4466-d26d-4966-af1f-ca4d087d0c4a',
        'parameters': event
    }
    data_header = {
        "Content-Type": "application/json;charset=UTF-8"
    }
    event_url = "https://danbee.ai/chatflow/54ae138f-fa8f-404f-8975-8ac6a3c45c35/eventFlow.do"
    res = requests.post(event_url,
                        data=json.dumps(data_send),
                        headers=data_header)
    data_receive = res.json()

    message = data_receive['responseSet']['result']['result'][0]['message']  # <- danbee json 포맷 분석 결과
    print("----- Event API ------")
    print(message)
    print("  ")

    return data_receive

# ----------------------------------------------------
# Danbee.ai에서 대답 구함
# ----------------------------------------------------
def get_answer_danbee(text, user_key):
    # --------------------------------
    # Danbee 요청
    # --------------------------------
    data_send = {
        'chatbot_id': 'c54e4466-d26d-4966-af1f-ca4d087d0c4a',
        'input_sentence': text
    }
    data_header = {
        "Content-Type": "application/json;charset=UTF-8"
    }
    danbee_chatflow_url = 'https://danbee.ai/chatflow/engine.do'

    res = requests.post(danbee_chatflow_url,
                        data=json.dumps(data_send),
                        headers=data_header)
    # --------------------------------
    # 대답 처리
    # --------------------------------
    '''
    if res.resultStatus != requests.codes.ok:
        return ERROR_MESSAGE
    '''

    data_receive = res.json()

    message = data_receive['responseSet']['result']['result'][0]['message']


    #answer = data_receive['result']

    print("\n")
    #print(user_key, ": ", text)
    #print("      [receptionbot]", ": ", message)

    sentence = user_key + ": " + text
    print_kor(sentence)
    sentence = "      [receptionbot]: " + message
    print_kor(sentence)


    #print_kor(data_receive)

    return data_receive



# ----------------------------------------------------
# Dialogflow에서 대답 구함
# ----------------------------------------------------
def get_answer_dialogflow(text, user_key):
    # --------------------------------
    # Dialogflow에 요청
    # --------------------------------
    data_send = {
        'lang': 'ko',
        'query': text,
        'sessionId': user_key,
        'timezone': 'Asia/Seoul'
    }

    data_header = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer 9d10041bdb9c4c68a88b7899ca1540c1'  # Dialogflow의 Client access token 입력
    }

    dialogflow_url = 'https://api.dialogflow.com/v1/query?v=20150910'


    print('test ---- ')

    res = requests.post(dialogflow_url,
                        data=json.dumps(data_send),
                        headers=data_header)

    # --------------------------------
    # 대답 처리
    # --------------------------------
    if res.status_code != requests.codes.ok:
        return ERROR_MESSAGE

    data_receive = res.json()
    answer = data_receive['result']


    #print(user_key, ": ", text)
    #print("      [receptionbot]", ": ", answer)
    print_kor(user_key + ": " + text)
    print_kor("      [receptionbot]: " + answer)


    return answer


# ----------------------------------------------------
# POST test to heroku for database
# ----------------------------------------------------
def test_post(name):
    # --------------------------------
    # 요청
    # --------------------------------
    data_send = {
        'name': name
    }

    data_header = {
        'Content-Type': 'application/json; charset=utf-8'
    }

    dialogflow_url = 'https://heroku-dialogflow-chatbot.herokuapp.com/message_danbee'


    res = requests.post(dialogflow_url,
                        data=json.dumps(data_send),
                        headers=data_header)

    # --------------------------------
    # 대답 처리
    # --------------------------------
    if res.status_code != requests.codes.ok:
        return ERROR_MESSAGE

    data_receive = res.json()

    #print(data_receive)

    print('----------  Test from heroku -----------')
    print(json.dumps(data_receive, indent=4, ensure_ascii=False))
    print('----------------------------------------')


# ----------------------------------------------------
# database from CSV file
# ----------------------------------------------------
def get_datatbase(kind_of_guide):
    filename = 'RMI_researchers.csv'

    with open(filename, 'r', encoding='UTF-8-sig') as f:
        csv_data = csv.reader(f, delimiter=',')
        print("-------------")
        dict = {}
        row_cnt = 0
        for row in csv_data:
            row_cnt = row_cnt + 1
            if row_cnt == 1:
                key = row
            else:
                for i in range(0, len(row), 1):
                    if i == 0:
                        # print(dict_name)
                        dict_info = {}
                    else:
                        dict_info.update({key[i]: row[i]})
                        # print(dict_info)
                dict.update({row[0]: dict_info})
                # print("dict_name = ", dict_name)

    #json_data = json.dumps(dict, indent=4, ensure_ascii=False)
    #print(json_data)


    return dict


def web_request():
    #while True:
        try:
            '''
            url = 'https://heroku-dialogflow-chatbot.herokuapp.com'
            # server content-type = application/json
            # r = requests.post('http://%s:8008/curlc' % url, json=web_data)

            web_data = {
                'user_key': 'DeepTasK',
                'content': '안녕하세요'
            }

            res = requests.post(url, json=web_data)
            '''

            # ------------------------
            # getting information of person(name) from database
            # ------------------------
            kind_of_guide = 'person'
            db = get_datatbase(kind_of_guide)
            #json_data = json.dumps(db, indent=4, ensure_ascii=False)


            # --------------------------------
            # Start Chat with Dialogflow API
            # --------------------------------
            user_key = 'DeepTasK'


            #content = ' '
            #res = get_answer(content, user_key)

            content = '안녕하세요'
            res = get_answer_danbee(content, user_key)

            content = '장'
            res = get_answer_danbee(content, user_key)

            return

            content = '안녕하세요'
            res = get_answer_danbee(content, user_key)

            content = '사람'
            res = get_answer_danbee(content, user_key)

            content = '임윤섭 박사님이 어디 계신가요?'
            res = get_answer_danbee(content, user_key)

            name = res['responseSet']['result']['parameters']['person_to_visit']
            # ------------------------
            # 최종석 박사 -> 최종석
            # 최종석 -> 최종석
            # ------------------------
            name = name.split()
            name = name[0]
            #print(name)



            '''
            content = '안녕하세요'
            res = get_answer_dialogflow(content, user_key)

            content = '최종석 박사님이 어디 계신가요?'
            res = get_answer_dialogflow(content, user_key)

#            content = '네.'
#            res = get_answer_dialogflow(content, user_key)

            content = '아니오.'
            res = get_answer_dialogflow(content, user_key)

            content = '최종석 박사님이요'
            res = get_answer_dialogflow(content, user_key)
            '''




            print('============= print from internal process ==================')

            # ------------------------
            # database에 해당 name의 사람이 있으면 그 사람의 information을 갖고 오고,
            # ''     ''      ''     ''  없으면 ERROR를 갖고 온다.
            # ------------------------
            try:
                info = db[name]
                #print('   information about ', name, ': ', json.dumps(info, indent=4, ensure_ascii=False))
            except:
                print('죄송합니다만, KIST 국제협력관에서 ', name, '님의 정보를 찾을 수 없습니다.')
                info = 'ERROR'

            answer = {
                'name': name,
                'information': info
            }
            print(json.dumps(answer, indent=4, ensure_ascii=False))

            print('======================================')


            # Heroku 서버 POST 테스트
            test_post(name)


        except Exception as e:
            pass

def speech_ui(stt_enable=1, tts_enable=1):

    # --------------------------------
    # Start Chat with Dialogflow API
    # --------------------------------
    user_key = 'DeepTasK'


    # --------------------------------
    # Create NaverTTS Class
    tts = NaverTTS(0,-1)    # Create a NaverTTS() class from tts/naver_tts.py
    #tts.play("안녕하십니까?")


    if stt_enable == 1:
        # 음성인식인 경우 무한 loop
        flag = True
        gsp = gspeech.Gspeech()
    else:
        # 음성인식 아닌 경우, 테스트 query에 대해 문장 단위로 테스트
        query = ["안녕",
                 "사람이요",
                 "최종석 박사님이요",
                 "아나스타샤를 찾으러 왔어요",
                 "홍길동님을 찾으러 왔어요",
                 #"여진구 박사님이요",
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
            res = get_answer_danbee(content, user_key)
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
                    db = get_datatbase(kind_of_guide)
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
                gsp = gspeech.Gspeech()
            pass




#----------------------------------------------------
# 메인 함수
#----------------------------------------------------
if __name__ == '__main__':

    stt_enable = 0  # 0: Disable speech recognition (STT), 1: Enable it
    tts_enable = 0  # 0: Disable speech synthesis (TTS),   1: Enable it

    speech_ui(stt_enable, tts_enable)
    #web_request()
