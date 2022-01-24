FROM ubuntu:20.04

RUN apt-get update \
&& apt-get install -y python \
&& apt-get install -y python3-pip

WORKDIR /code/

ADD requirements.txt /code/requirements.txt
RUN python3 -m pip install -r requirements.txt

ADD main.py /code/main.py
ADD app/ /code/app/


VOLUME /code/data

ENTRYPOINT ["python3", "-u", "main.py"]