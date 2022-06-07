FROM python:3.8

WORKDIR /black_passport
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY . .

# install dependencies
RUN pip install -r requirements.txt

#
#RUN apk add --update --no--cache --virtual .tmp-build-deps \
#        gcc libc-dev linux-headers postgresql-dev && \
#    pip install --no-cache-dir -r requirements.txt
#RUN apt-get update -y
#RUN apt-get upgrade -y
#
#WORKDIR /black_passport
#COPY . .
#RUN pip install -r requirements.txt
##COPY ./black_passport ./black_passport
##COPY ./passport ./passport
##COPY ./venv ./venv
##COPY ./manage.py ./
#
#CMD [ 'python3', './manage.py', 'runserver']