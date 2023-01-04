# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /EveryRockBeatEver

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "--app", "EveryDrumBeatEver", "run", "--host=0.0.0.0"]