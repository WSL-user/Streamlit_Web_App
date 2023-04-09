# app/Dockerfile

FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
        curl \
        software-properties-common \
        git \
        && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./requirements.txt

COPY ./streamlit_share.py ./streamlit_share.py

RUN pip3 install -r requirements.txt

#TODO ポート番号を空いてるものに変更
EXPOSE 18840

#TODO ポート番号を空いてるものに変更
HEALTHCHECK CMD curl --fail http://localhost:18840/_stcore/health

#TODO ポート番号を空いてるものに変更
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=18840", "--server.address=0.0.0.0"]