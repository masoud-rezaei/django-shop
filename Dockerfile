# Pull base image
FROM python:alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
ADD requirements.txt /code/
WORKDIR /code

#ADD secrets.json /code/
RUN apk add --update --no-cache curl jq py3-configobj py3-pip py3-setuptools python3 python3-dev build-base 
RUN apk add py3-reportlab openssl-dev ca-certificates \ 
    pango-dev  libpng-dev py3-pillow \
    make automake libffi-dev gcc linux-headers g++ py3-brotli  py3-cffi musl-dev postgresql-dev zlib-dev jpeg-dev py3-wheel
RUN pip3 install -r requirements.txt  
 #msttcorefonts-installer fontconfig zopfli  gettext libxml2-dev libxslt-dev\ pango gdk-pixbuf-dev cario-dev
    #uwsgi uwsgi-python3 dumb-init fontconfig-dev harfbuzz-dev  shared-mime-info openjpeg-dev freetype-dev
# py3-wheel    python3 --update subversion python3-cffi rabbitmq-c
EXPOSE 8000
CMD  python manage.py makemigrations --noinput && \
    python manage.py migrate --noinput &&\
    python manage.py collectstatic --noinput &&\
    python manage.py createsuperuser --user admin --email admin@localhost --noinput && \
    python manage.py runserver 0.0.0.0:8000  --noinput 
# Copy project
COPY . /code/
