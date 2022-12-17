FROM python:3

# Should really move this to requirements.txt...
RUN pip3 install flask requests discord.py pyyaml markovify crawler-py pillow

ADD . /app

WORKDIR /app

CMD ["python3", "."]
