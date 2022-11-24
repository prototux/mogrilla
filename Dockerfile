FROM python:3

RUN pip3 install flask requests discord.py pyyaml markovify crawler-py

ADD . /app

WORKDIR /app

CMD ["python3", "."]
