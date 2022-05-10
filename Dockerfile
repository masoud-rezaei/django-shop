# Pull base image
FROM python:alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
#ADD secrets.json /code/
RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev 
#RUN pip install --upgrade pip 
RUN pip install -r requirements.txt   
#EXPOSE 8000
#CMD  python manage.py makemigrations --noinput && \
 #    python manage.py migrate --noinput &&\
  #   python manage.py collectstatic --noinput &&\
   #  python manage.py createsuperuser --user admin --email admin@localhost --noinput && \
    # python manage.py runserver 0.0.0.0:8000  --noinput 
# Copy project
COPY . /code/
