FROM python:3.8

ENV PYTHONBUFFERED 1

RUN apt update
# Dependencies for psycopgy2 and mod_wsgi python package
RUN apt install -y python3-dev libpq-dev gcc bash apache2 apache2-dev

# This should be a module
RUN mkdir /app
WORKDIR /app
ADD . /app
# This should be a soft link to a file from the module
RUN mkdir /etc/inite && cp /app/variables.json /etc/inite

RUN python -m venv venv
RUN /app/venv/bin/python -m pip install --upgrade pip
RUN . venv/bin/activate && pip install -r requirements.txt

RUN useradd app && chown -R app:app /app

CMD su app -s /bin/bash -c '. /app/venv/bin/activate && \
                            mod_wsgi-express start-server \ 
                            --url-alias /static ./static /app/inite/wsgi.py'
