# NOTE!!!
# Develop Dockerfile. Remember to: 
#  1 -> . /venv/bin/activate
#  2 -> python manage.py makemigrations portal
#  3 -> python manage.py migrate

FROM python:3

ENV PYTHONBUFFERED 1

ENV DEBIAN_FRONTEND=noninteractive

RUN apt -y update

# Dependencies for psycopgy2 and mod_wsgi python package
RUN apt install -yyy    libpq-dev    \
                        gcc          \
                        bash         \
                        apache2      \
                        apache2-dev  \
                        postgresql   \
                        curl

RUN python3 -m venv /venv && \
	/venv/bin/python3 -m pip install --upgrade pip && \
    . /venv/bin/activate && \
    pip install $(curl https://raw.githubusercontent.com/aucoop/inite/dockerize/web/requirements.txt)

RUN mkdir /webapp
WORKDIR /webapp

RUN useradd webapp && chown -R webapp:webapp /webapp/
 
# Create a link to an existing file (with docker approach might not make sense)
RUN mkdir /etc/inite && ln -s /webapp/variables.json /etc/inite/variables.json

CMD su webapp -s /bin/bash -c ' . /venv/bin/activate && \
								python3 manage.py makemigrations && \
								python3 manage.py migrate portal && \
								mod_wsgi-express start-server --url-alias /static ./static /webapp/inite/wsgi.py'
