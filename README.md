# Broadcasting sentiment analysis to UDINUS

This is a simple example of how to broadcast sentiment analysis to UDINUS using Django and Deep Learning.

## Installation
```shell
$ git clone https://github.com/danangharissetiawan/sentiment_analysis_udinus.git
```

## Usage
```shell
$ cd sentiment_analysis_udinus
```

### Setup virtual environment
```shell
$ python3 -m venv venv

$ source venv/bin/activate # for linux
$ venv\Scripts\activate # for windows
```

### Install requirements
```shell
$ pip install -r requirements.txt
```

### migrate database
```shell
$ python manage.py makemigrations
$ python manage.py migrate
```

### Create superuser
```shell
$ python manage.py createsuperuser
```

### Run server
```shell
$ python manage.py runserver
```
