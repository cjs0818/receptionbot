# -*- coding: utf-8 -*-

import requests
import json


def web_request():
    #while True:
        try:

            # --------------------------------
            # 요청
            # --------------------------------
            data_send_query = {
                'name': '최종석'
            }

            data_header = {
                'Content-Type': 'application/json; charset=utf-8'
            }

            dialogflow_url = 'https://heroku-dialogflow-chatbot.herokuapp.com/message_danbee'

            res = requests.post(dialogflow_url,
                                data=json.dumps(data_send_query),
                                headers=data_header)

            # --------------------------------
            # 대답 처리
            # --------------------------------
            if res.status_code != requests.codes.ok:
                return ERROR_MESSAGE

            data_receive = res.json()

            #print(data_receive)
            print(json.dumps(data_receive, indent=4, ensure_ascii=False))



        except Exception as e:
            pass

#----------------------------------------------------
# 메인 함수
#----------------------------------------------------
if __name__ == '__main__':

    web_request()
