FROM python:3.6-stretch

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD ./ /code/

CMD ['scripts/run.sh']