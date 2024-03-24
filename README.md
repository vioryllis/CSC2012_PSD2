# CSC2012_PSD2
```
NEARBYFARMER / FARAWAYFARMER
This is a webapp that controls a hydroponic plant setup equipped with sensors for sensing water level/nutrient levels. A M5StickCPlus is used as the microcontroller that sends data over from the sensors to this django server. The server will then store the data from the sensors into PostgreSQL. The controls will send post requests over to the server side which then sends signals over to the M5Stick to a) water the plant, b) fertilize the plant and c) turn on/off the auto watering system.
```

## remember to make your own venv
```
"C:\Users\USER\AppData\Local\Programs\Python\Python310\python.exe" -m venv venv
or
python -m venv venv
```

##  remember to pip install django and other requirements

```
can choose to install from either requirements file:
pip install -r requirements.txt (in the psd2 folder)
pip install -r requirements.txt (in the base folder)
```

### three containers for three microservices
```
(api container) Data Ingestion + Sensor Management Service: Retrieve data and store into postgres, setup REST API for controls
(postgres container) for database
(faraway farmer container) Data Processing Service: Display user interface and controls, pulls data from database
```

### to run the server (RUN FIRST before api side)
If running locally, edit the following code in ```settings.py``` file to match your database settings:
```
DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': 'farawayfarmer', # database name (must match with api side)
        'USER': 'example',
        'PASSWORD': 'example',
        'HOST': 'db',
        #'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
```
python manage.py migrate
```
```
python manage.py runserver localhost:8001
```

### to run api side (RUN AFTER psd2 side)
```
cd into api folder and create a .env file
then add these details inside the file: (edit the fields according to your own postgres details)

# Postgres database settings
POSTGRES_DATABASE_NAME = 'farawayfarmer' # both sides must match db names (api and psd2)
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = '1234'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'

for local postgres, create database with the same name as POSTGRES_DATABASE_NAME inside pgadmin4.

then run py manage.py migrate

if you are using m5stick to send data over, you have to specify 0.0.0.0 behind to allow connection from other networks:

py manage.py runserver 0.0.0.0:8000

```

### to run docker container
From the root directory, run
```
docker-compose up
```
# end
