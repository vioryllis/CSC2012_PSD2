# CSC2012_PSD2

## remember to make your own venv
```
"C:\Users\USER\AppData\Local\Programs\Python\Python310\python.exe" -m venv venv
or
python -m venv venv
```

##  remember to pip install django

```
pip install -r requirements.txt (in the psd2 folder)
```

### should create a different branch for each microservice we have
```
(api container) Data Ingestion + Sensor Management Service: Retrieve data and store into postgres, setup REST API for controls
(postgres container) for database
(faraway farmer container) Data Processing Service: Display user interface and controls
```

### to run api side
```
cd into api folder and create a .env file
then add these details inside the file: (edit the fields according to your own postgres details)

# Postgres database settings
POSTGRES_DATABASE_NAME = 'nearbyfarmer'
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = '1234'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'

for local postgres, create database with the same name as POSTGRES_DATABASE_NAME inside pgadmin4.

then run py manage.py migrate

if you are using m5stick to send data over, you have to specify 0.0.0.0 behind to allow connection from other networks:

py manage.py runserver 0.0.0.0:8000

```

### to run the server
If running locally, edit the following code in ```settings.py``` file to match your database settings:
```
DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': 'farawayfarmer', # database name
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
python manage.py runserver
```


### to run docker container
From the root directory, run
```
docker-compose up
```
# end
