# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /EveryRockBeatEver

COPY requirements.txt requirements.txt
# ALSA RUN Dialog -- WIP for CLOUD Deployment (Production)
# RUN apt-get update && apt-get install -yq \
#    libgtk2.0-dev \
#    libasound2 \
#    alsa-tools \
#    && pip3 install -r requirements.txt
# && rm -rf /var/lib/apt/lists/* \
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "--app", "EveryRockBeatEver", "run", "--host=0.0.0.0"]