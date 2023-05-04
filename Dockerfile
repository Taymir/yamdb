FROM python:3.9.6

RUN mkdir /code
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt
COPY . /code
WORKDIR /code
RUN cp docker.env .env
CMD gunicorn api_yamdb.whitenoiseWSGI:application --bind 0.0.0.0:8000