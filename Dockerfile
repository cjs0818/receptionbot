# docker pull pristine70/receptionbot

# 베이스 이미지로 ubuntu:16.04 사용 
FROM ubuntu:16.04

# 메인테이너 정보 (옵션)
MAINTAINER <your-nickname> <<your-email>>

# 환경변수 설정 (옵션)
ENV PATH /usr/local/bin:$PATH
ENV LANG C.UTF-8

# 기본 패키지들 설치 및 Python 3 설치
# Python3.6 has problem
RUN apt-get -qq -y update
RUN apt-get install -y software-properties-common

RUN add-apt-repository -y ppa:fkrull/deadsnakes
RUN apt-get -qq -y update
RUN apt-get install -y --no-install-recommends python3 python3-dev python3-pip python3-setuptools python3-wheel gcc
RUN apt-get install -y git curl
RUN apt-get install -y portaudio19-dev
RUN apt-get install -y vlc browser-plugin-vlc
RUN sed -i 's/geteuid/getppid/' /usr/bin/vlc


# pip 업그레이드
RUN python3 -m pip install pip --upgrade

# 여러분의 현재 디렉토리의 모든 파일들을 도커 컨테이너의 /receptionbot 디렉토리로 복사 (원하는 디렉토리로 설정해도 됨)
ADD . /receptionbot

# 5000번 포트 개방 (Flask 웹 애플리케이션을 5000번 포트에서 띄움)
EXPOSE 5000

# 작업 디렉토리로 이동
WORKDIR /receptionbot

# 작업 디렉토리에 있는 requirements.txt로 패키지 설치
RUN pip3 install -r requirements.txt


# Install Google Cloud SDK
RUN export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)" && \
    echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    apt-get update -y && apt-get install google-cloud-sdk -y

#RUN gcloud iam service-accounts keys create ~/jschoi_gcloud_service_accounts_key.json --iam-account jschoi@chatbot-215901.iam.gserviceaccount.com

RUN echo "export GOOGLE_APPLICATION_CREDENTIALS=/receptionbot/.config/gcloud/application_default_credentials.json" >> ~/.bashrc  #  필자와 경로가 다를 수 있으니 주의


# 컨테이너에서 실행될 명령어. 컨테이거나 실행되면 app.py를 실행시킨다.
CMD python3 app.py
