FROM python:3.10
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./black_passport ./black_passport

CMD [ 'python3', './black_passport/manage.py', 'runserver']