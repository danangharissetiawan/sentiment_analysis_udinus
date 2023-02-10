FROM  python:3.10

ENV  PYTHONDONTWRITEBYTECODE  1
ENV  PYTHONUNBUFFERED  1

WORKDIR  /code

COPY  requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# RUN python manage.py collectstatic
# RUN python manage.py makemigrations && python manage.py migrate

COPY  . /code/

CMD gunicorn --bind 0.0.0.0:$PORT config.wsgi