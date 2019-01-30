FROM python:3.7.2

RUN pip install requests
RUN pip install flask
RUN pip install elasticsearch

ADD kawaii.py kawaii.py
ADD server.py server.py

CMD python3 server.py
